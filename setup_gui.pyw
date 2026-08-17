#!/usr/bin/env python3
"""IEM-PM Setup Wizard -- a guided, no-terminal-required install/first-run experience.

Does the same underlying work as setup.ps1/setup.sh (install dependencies, create folders,
check Claude Code) through a small window with buttons instead of scrolling console text, and
adds guided file-picking for standards/evidence that the console scripts always left as a
manual "go find the folder yourself" step. Also lets the user choose where IEM-PM actually
lives, rather than silently treating wherever the ZIP happened to be extracted (often
Downloads) as the permanent install location.

Prerequisite this cannot eliminate: Python itself must already be installed and working for
this window to even open (tkinter ships with Python, but Python doesn't self-install).
setup.bat/setup.sh try this first and fall back to the console flow if tkinter import fails
(e.g. a Linux Python built without the optional tk package) or Python itself is missing.
"""
import os
import queue
import shutil
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Where this script is currently running from -- the extraction point, not necessarily where
# the user wants IEM-PM to actually live long-term. LocationPage lets them redirect that.
SOURCE_ROOT = Path(__file__).resolve().parent
DEFAULT_INSTALL_SUGGESTION = Path.home() / "Documents" / "IEM-PM"

FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SMALL = ("Segoe UI", 9)
PAD = 20

# Never copied when relocating to a chosen install folder.
COPY_SKIP_NAMES = {".git", "__pycache__", ".vscode", ".DS_Store"}


def python_launcher() -> str:
    """The Python executable currently running this script -- reuse it for pip/subprocess
    calls instead of guessing "python" vs "python3" is on PATH the same way."""
    return sys.executable


def merge_copy_tree(src: Path, dst: Path, progress_cb=None):
    """Copy src's contents into dst, creating dst if needed. Never overwrites a file that
    already exists at the destination -- a relocate onto a folder that already has a real
    IEM-PM install (real standards, real evidence) must not clobber it. progress_cb(name) is
    called once per file copied, for status display."""
    for item in src.rglob("*"):
        if any(part in COPY_SKIP_NAMES for part in item.relative_to(src).parts):
            continue
        rel = item.relative_to(src)
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            if progress_cb:
                progress_cb(str(rel))


class Page(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=PAD)
        self.app = app


class WelcomePage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="IEM-PM Setup", font=FONT_TITLE).pack(anchor="w", pady=(0, 10))
        ttk.Label(
            self,
            text=(
                "This wizard gets IEM-PM running on this computer: choose where it lives, "
                "install what it needs, and help you add your organization's real PM "
                "standards. Takes a few minutes, once per computer."
            ),
            font=FONT_BODY, wraplength=520, justify="left",
        ).pack(anchor="w", pady=(0, 20))
        ttk.Button(self, text="Get Started  →", command=lambda: app.show("LocationPage")).pack(
            anchor="e"
        )


class LocationPage(Page):
    """Where IEM-PM actually lives. Defaults to a suggested permanent home, not wherever the
    ZIP was extracted -- but never silently picks that for the user."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="Where should IEM-PM live?", font=FONT_TITLE).pack(
            anchor="w", pady=(0, 10)
        )
        ttk.Label(
            self,
            text=(
                "Pick any folder. If it's different from where you unzipped this, everything "
                "will be copied there and this wizard will continue from the new location -- "
                "nothing already there gets overwritten."
            ),
            font=FONT_BODY, wraplength=520, justify="left",
        ).pack(anchor="w", pady=(0, 15))

        self.path_var = tk.StringVar(value=str(app.install_root))
        row = ttk.Frame(self)
        row.pack(fill="x", pady=(0, 10))
        ttk.Entry(row, textvariable=self.path_var).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Browse…", command=self._browse).pack(side="left", padx=(8, 0))

        ttk.Label(
            self,
            text=f"Currently running from:\n{SOURCE_ROOT}",
            font=FONT_SMALL, foreground="#555",
        ).pack(anchor="w", pady=(0, 15))

        self.status_label = ttk.Label(self, text="", font=FONT_SMALL, foreground="#555")
        self.status_label.pack(anchor="w")
        self.progress = ttk.Progressbar(self, mode="indeterminate")

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(20, 0))
        ttk.Button(nav, text="← Back", command=lambda: app.show("WelcomePage")).pack(side="left")
        self.next_btn = ttk.Button(nav, text="Continue  →", command=self._confirm)
        self.next_btn.pack(side="right")

    def _browse(self):
        chosen = filedialog.askdirectory(
            title="Choose where IEM-PM should live", initialdir=self.path_var.get()
        )
        if chosen:
            self.path_var.set(chosen)

    def _confirm(self):
        chosen = Path(self.path_var.get().strip()).expanduser()
        if not chosen:
            messagebox.showerror("No folder chosen", "Pick a folder first.")
            return
        try:
            chosen.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Can't use that folder", str(e))
            return

        if chosen.resolve() == SOURCE_ROOT.resolve():
            self.app.install_root = SOURCE_ROOT
            self.app.show("CheckPage")
            return

        self.next_btn.configure(state="disabled")
        self.status_label.configure(text="Copying IEM-PM to the new location…")
        self.progress.pack(fill="x", pady=(10, 0))
        self.progress.start(12)

        def worker():
            try:
                merge_copy_tree(SOURCE_ROOT, chosen)
                self.after(0, lambda: self._copy_done(chosen, None))
            except Exception as e:
                self.after(0, lambda: self._copy_done(chosen, e))

        threading.Thread(target=worker, daemon=True).start()

    def _copy_done(self, chosen, error):
        self.progress.stop()
        self.next_btn.configure(state="normal")
        if error:
            self.status_label.configure(text=f"Copy failed: {error}")
            messagebox.showerror("Copy failed", str(error))
            return
        self.app.install_root = chosen
        self.app.show("CheckPage")


class CheckPage(Page):
    """Installs dependencies and checks for Claude Code. Runs pip install in a background
    thread -- Tkinter isn't thread-safe, so the worker thread only ever posts status strings
    onto a queue, and a periodic after() poll on the main thread is what actually touches
    widgets."""

    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="Checking your computer", font=FONT_TITLE).pack(anchor="w", pady=(0, 5))
        ttk.Label(
            self, text=f"Installing to: {app.install_root}", font=FONT_SMALL, foreground="#555"
        ).pack(anchor="w", pady=(0, 15))

        self.rows = {}
        for key, label in [
            ("python", "Python"),
            ("deps", "Dependencies"),
            ("claude", "Claude Code"),
        ]:
            row = ttk.Frame(self)
            row.pack(fill="x", pady=4)
            status = ttk.Label(row, text="⏳", width=3, font=FONT_BODY)
            status.pack(side="left")
            ttk.Label(row, text=label, font=FONT_BODY).pack(side="left")
            detail = ttk.Label(row, text="", font=FONT_SMALL, foreground="#555")
            detail.pack(side="left", padx=(10, 0))
            self.rows[key] = (status, detail)

        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", pady=(15, 5))

        self.log = tk.Text(self, height=6, font=("Consolas", 8), state="disabled", bg="#f5f5f5")
        self.log.pack(fill="both", expand=True, pady=(5, 15))

        nav = ttk.Frame(self)
        nav.pack(fill="x")
        ttk.Button(nav, text="← Back", command=lambda: app.show("LocationPage")).pack(side="left")
        self.next_btn = ttk.Button(
            nav, text="Continue  →", command=lambda: app.show("StandardsPage"), state="disabled"
        )
        self.next_btn.pack(side="right")

        self._q = queue.Queue()
        self._started = False

    def on_show(self):
        if self._started:
            return
        self._started = True
        self._set_row("python", "ok", "Found (running this wizard)")
        self.progress.start(12)
        threading.Thread(target=self._worker, daemon=True).start()
        self.after(100, self._poll)

    def _append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_row(self, key, state, detail=""):
        status, detail_label = self.rows[key]
        status.configure(text={"ok": "✅", "warn": "⚠️", "fail": "❌"}.get(state, "⏳"))
        detail_label.configure(text=detail)

    def _worker(self):
        # Defensive, not redundant: LocationPage always creates install_root before getting
        # here, but subprocess.run's cwd= fails outright (WinError 267) if the directory
        # somehow doesn't exist yet -- caught by testing this page directly, out of sequence.
        self.app.install_root.mkdir(parents=True, exist_ok=True)
        try:
            result = subprocess.run(
                [python_launcher(), "-m", "pip", "install", "-r", str(self.app.requirements_file)],
                cwd=str(self.app.install_root), capture_output=True, text=True,
            )
            self._q.put(("log", result.stdout + result.stderr))
            if result.returncode == 0:
                self._q.put(("deps", "ok", "Installed"))
            else:
                self._q.put(("deps", "fail", "See log below -- try running setup.bat instead"))
        except Exception as e:
            self._q.put(("log", str(e)))
            self._q.put(("deps", "fail", "Failed -- see log below"))

        for folder in (self.app.audit_dir, self.app.knowledge_dir):
            folder.mkdir(parents=True, exist_ok=True)

        claude = shutil.which("claude")
        if claude:
            self._q.put(("claude", "ok", "Found"))
        else:
            self._q.put(("claude", "warn", "Not found -- install from claude.com/claude-code"))

        self._q.put(("done", None))

    def _poll(self):
        try:
            while True:
                item = self._q.get_nowait()
                if item[0] == "log":
                    self._append_log(item[1])
                elif item[0] == "done":
                    self.progress.stop()
                    self.next_btn.configure(state="normal")
                else:
                    self._set_row(item[0], item[1], item[2])
        except queue.Empty:
            pass
        self.after(150, self._poll)


class StandardsPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="Add your standards", font=FONT_TITLE).pack(anchor="w", pady=(0, 10))
        ttk.Label(
            self,
            text=(
                "IEM-PM audits against your organization's own real standards -- PMBOK, PRINCE2, "
                "ISO 21502, or your own methodology. It ships with none of its own, on purpose "
                "(these are licensed content, not this tool's to redistribute). Nothing you add "
                "here ever leaves this computer."
            ),
            font=FONT_BODY, wraplength=520, justify="left",
        ).pack(anchor="w", pady=(0, 15))

        self.listbox = tk.Listbox(self, height=6)
        self.listbox.pack(fill="both", expand=True, pady=(0, 10))
        self._refresh_list()

        ttk.Button(self, text="Add standard files…", command=self._add_files).pack(anchor="w")

        ttk.Label(
            self, text="This step is optional here -- you can add standards later too.",
            font=FONT_SMALL, foreground="#555",
        ).pack(anchor="w", pady=(15, 0))

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(20, 0))
        ttk.Button(nav, text="← Back", command=lambda: app.show("CheckPage")).pack(side="left")
        ttk.Button(
            nav, text="Continue  →", command=lambda: app.show("EvidencePage")
        ).pack(side="right")

    def _refresh_list(self):
        self.listbox.delete(0, "end")
        knowledge_dir = self.app.knowledge_dir
        if knowledge_dir.exists():
            for f in sorted(knowledge_dir.rglob("*")):
                if f.is_file() and f.name != "README.md":
                    self.listbox.insert("end", str(f.relative_to(knowledge_dir)))

    def _add_files(self):
        paths = filedialog.askopenfilenames(
            title="Choose your organization's standards (PDF, Word, or Markdown)",
            filetypes=[("Documents", "*.pdf *.docx *.doc *.md *.txt"), ("All files", "*.*")],
        )
        if not paths:
            return
        knowledge_dir = self.app.knowledge_dir
        knowledge_dir.mkdir(parents=True, exist_ok=True)
        errors = []
        for p in paths:
            src = Path(p)
            try:
                shutil.copy2(src, knowledge_dir / src.name)
            except Exception as e:
                errors.append(f"{src.name}: {e}")
        self._refresh_list()
        if errors:
            messagebox.showwarning("Some files didn't copy", "\n".join(errors))


class EvidencePage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="Set up a project to audit", font=FONT_TITLE).pack(anchor="w", pady=(0, 10))
        ttk.Label(
            self,
            text="Give this audit project a name, then add the real delivery evidence "
                 "(schedules, RAID logs, status reports) you want audited.",
            font=FONT_BODY, wraplength=520, justify="left",
        ).pack(anchor="w", pady=(0, 15))

        name_row = ttk.Frame(self)
        name_row.pack(fill="x", pady=(0, 10))
        ttk.Label(name_row, text="Project name:", font=FONT_BODY).pack(side="left")
        self.name_var = tk.StringVar(value="My Project")
        ttk.Entry(name_row, textvariable=self.name_var, width=30).pack(side="left", padx=(10, 0))

        self.listbox = tk.Listbox(self, height=6)
        self.listbox.pack(fill="both", expand=True, pady=(0, 10))

        ttk.Button(self, text="Add evidence files…", command=self._add_files).pack(anchor="w")

        ttk.Label(
            self, text="Optional here too -- you can create project folders any time.",
            font=FONT_SMALL, foreground="#555",
        ).pack(anchor="w", pady=(15, 0))

        nav = ttk.Frame(self)
        nav.pack(fill="x", pady=(20, 0))
        ttk.Button(nav, text="← Back", command=lambda: app.show("StandardsPage")).pack(side="left")
        ttk.Button(nav, text="Continue  →", command=lambda: app.show("FinishPage")).pack(side="right")

    def _evidence_dir(self) -> Path:
        name = self.name_var.get().strip() or "My Project"
        return self.app.audit_dir / name / "evidence"

    def _add_files(self):
        paths = filedialog.askopenfilenames(title="Choose delivery evidence files")
        if not paths:
            return
        target = self._evidence_dir()
        target.mkdir(parents=True, exist_ok=True)
        errors = []
        for p in paths:
            src = Path(p)
            try:
                shutil.copy2(src, target / src.name)
            except Exception as e:
                errors.append(f"{src.name}: {e}")
        self.listbox.delete(0, "end")
        for f in sorted(target.glob("*")):
            if f.is_file():
                self.listbox.insert("end", f.name)
        if errors:
            messagebox.showwarning("Some files didn't copy", "\n".join(errors))


class FinishPage(Page):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        ttk.Label(self, text="You're set up", font=FONT_TITLE).pack(anchor="w", pady=(0, 10))
        ttk.Label(
            self,
            text=f"IEM-PM lives at:\n{app.install_root}\n\n"
                 "Open Claude Code from inside that exact folder, then paste this in:",
            font=FONT_BODY, wraplength=520, justify="left",
        ).pack(anchor="w", pady=(0, 10))

        prompt_row = ttk.Frame(self)
        prompt_row.pack(fill="x", pady=(0, 15))
        self.prompt_text = "Audit my project using the intelligence-engine skill"
        entry = ttk.Entry(prompt_row, font=("Consolas", 10))
        entry.insert(0, self.prompt_text)
        entry.configure(state="readonly")
        entry.pack(side="left", fill="x", expand=True)
        ttk.Button(prompt_row, text="Copy", command=self._copy_prompt).pack(side="left", padx=(8, 0))

        ttk.Button(
            self, text="Open the full User Guide", command=self._open_guide
        ).pack(anchor="w", pady=(0, 8))
        ttk.Button(
            self, text="Open this folder", command=self._open_folder
        ).pack(anchor="w")

        ttk.Button(self, text="Close", command=self.app.master.destroy).pack(anchor="e", pady=(30, 0))

    def _copy_prompt(self):
        self.clipboard_clear()
        self.clipboard_append(self.prompt_text)
        messagebox.showinfo("Copied", "Prompt copied -- paste it into Claude Code.")

    def _open_guide(self):
        guide = self.app.user_guide
        if guide.exists():
            webbrowser.open(guide.as_uri())
        else:
            messagebox.showerror("Not found", f"Couldn't find {guide}")

    def _open_folder(self):
        target = self.app.install_root
        try:
            if sys.platform == "win32":
                os.startfile(str(target))  # noqa: S606 -- local folder, not user input
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(target)])
            else:
                subprocess.Popen(["xdg-open", str(target)])
        except Exception as e:
            messagebox.showerror("Couldn't open folder", str(e))


class App:
    PAGE_CLASSES = {
        cls.__name__: cls
        for cls in [WelcomePage, LocationPage, CheckPage, StandardsPage, EvidencePage, FinishPage]
    }

    def __init__(self, master):
        self.master = master
        master.title("IEM-PM Setup")
        master.geometry("600x580")
        master.minsize(560, 540)

        # Defaults to a real suggested home, not silently wherever the ZIP was extracted --
        # LocationPage is what actually lets the user confirm or change this. Every other
        # page reads paths through the properties below rather than a module-level constant,
        # so relocating mid-wizard (LocationPage's job) is the only place that has to know.
        self.install_root = DEFAULT_INSTALL_SUGGESTION

        self.container = ttk.Frame(master)
        self.container.pack(fill="both", expand=True)
        self.current_frame = None

        self.show("WelcomePage")

    @property
    def knowledge_dir(self) -> Path:
        return self.install_root / "skills" / "intelligence-engine" / "knowledge"

    @property
    def audit_dir(self) -> Path:
        return self.install_root / "Audit"

    @property
    def requirements_file(self) -> Path:
        return self.install_root / "requirements.txt"

    @property
    def user_guide(self) -> Path:
        return self.install_root / "Public" / "IEM-PM-User-Guide.html"

    def show(self, name):
        # Only one page frame ever exists at a time -- deliberately not the common
        # "pre-create every page and tkraise() the one you want" pattern: on this Windows/
        # ttk theme combination that produced real visual bleed-through (a previous page's
        # content stayed partially rendered even though its show() was never called again),
        # confirmed via traceback logging before switching to this approach.
        if self.current_frame is not None:
            self.current_frame.destroy()
        frame = self.PAGE_CLASSES[name](self.container, self)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame
        if hasattr(frame, "on_show"):
            frame.on_show()


def main():
    root = tk.Tk()
    try:
        style = ttk.Style(root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
