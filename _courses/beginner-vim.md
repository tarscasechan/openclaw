---
title: Beginner Vim: Edit a Tiny Notes File
summary: A short, example-led introduction to Vim's modal editing loop.
---

# Beginner Vim: Edit a Tiny Notes File

**Goal:** make and revise a small `notes.txt` file without trying to learn all of Vim.

**Starting point:** you can use a terminal, but you do not need prior Vim experience.

**Course promise:** by the end, you can open Vim, survive the modes, make small edits, search, select text, save, and quit.

## Lesson 1: Start Vim and Leave Safely — command line

**Outcome:** Learner can open Vim and quit without panic.

The first pain in Vim is not editing. It is getting trapped in a full-screen program with no obvious exit.

Tiny example:

```sh
vim
```

You start on Vim's welcome screen. Press `:` to enter command-line mode, type `q`, then press Enter:

```vim
:q
```

**Try it:** Open Vim with `vim`, then quit with `:q`.

**What changed?** Vim commands often start from normal mode, and `:` lets you type a command.

**But:** Quitting an empty editor is not editing a real file.

## Lesson 2: Open a Real File — file buffer

**Outcome:** Learner can open a file and recognize the buffer they are editing.

Other editors often start with “open file.” Vim can start empty, but real work usually starts with a file path.

Tiny example:

```sh
vim notes.txt
```

If `notes.txt` does not exist, Vim opens a new buffer for that file.

**Try it:** Run `vim notes.txt`, then quit with `:q`.

**What changed?** A Vim buffer is the in-memory version of a file you may later save.

**But:** Opening a file still leaves you in normal mode, where typing letters does not insert text.

## Lesson 3: Enter Text and Return Home — normal mode

**Outcome:** Learner can move from normal mode to insert mode and back.

Vim is a modal editor: the same key can mean different things depending on the mode. This is the main difference from most editors.

Tiny example:

```txt
Today I learned Vim.
```

Press `i` to enter insert mode, type the sentence, then press Escape to return to normal mode.

**Try it:** In `notes.txt`, press `i`, type one line, then press Escape.

**What changed?** `i` starts inserting text; Escape gets you back to normal mode.

**But:** The text exists in Vim, but it is not safely written to disk yet.

## Lesson 4: Save or Quit Intentionally — write commands

**Outcome:** Learner can save, quit, or abandon changes deliberately.

Vim protects you from accidentally losing edits, so `:q` fails if the file has unsaved changes.

Tiny examples:

```vim
:w      " write/save
:q      " quit
:wq     " write and quit
:q!     " quit and discard changes
```

**Try it:** Add one line, press Escape, then save and quit with `:wq`.

**What changed?** Command-line mode handles file-level actions like writing and quitting.

**But:** Editing only at the cursor is slow; you need a few movement keys.

## Lesson 5: Move Before You Edit — motion

**Outcome:** Learner can move around a small file in normal mode.

Normal mode turns keys into actions. Before learning many commands, learn just enough movement to choose where the next edit happens.

Tiny example:

```txt
Vim is modal.
Escape returns to normal mode.
Small commands compose.
```

Useful keys:

```txt
h left   j down   k up   l right
0 start of line   $ end of line
w next word       b previous word
```

**Try it:** Open `notes.txt`, move to the second line with `j`, then move word by word with `w` and `b`.

**What changed?** In normal mode, movement is part of editing, not separate from it.

**But:** Sometimes you need to change a chunk, not just place the cursor.

## Lesson 6: Select Text Visually — visual mode

**Outcome:** Learner can select text and see the boundary of an edit.

Visual mode is useful when you are not ready to compose commands from memory. It makes the target visible.

Tiny example:

```txt
delete this phrase
```

Press `v` to enter visual mode, move with `w` or `l`, then press `d` to delete the selected text. Press Escape if you want to cancel.

**Try it:** Add a line with extra words, use `v` to select the extra words, then press `d`.

**What changed?** `v` lets you mark text first and choose the action second.

**But:** Finding text by moving one key at a time is tedious.

## Lesson 7: Find Text Quickly — search mode

**Outcome:** Learner can search inside a file and continue from the match.

Search mode answers the “where is that word?” pain without scrolling.

Tiny example:

```vim
/modal
```

Press `/`, type a search term, and press Enter. Use `n` for the next match and `N` for the previous match.

**Try it:** Search for `normal`, jump to the next match with `n`, then press Escape.

**What changed?** `/` moves the cursor by meaning, not by distance.

**But:** You now know the survival loop; the next course can teach editing grammar and composition.

## Minimal example artifact

Create `notes.txt` with this final content:

```txt
Today I learned Vim.
Vim is modal.
Escape returns to normal mode.
Search finds words quickly.
```

## Smoke test

A learner has passed if they can:

1. Run `vim notes.txt`.
2. Press `i`, add one sentence, and press Escape.
3. Save with `:w`.
4. Search with `/Vim`.
5. Select one word with `v` and movement keys.
6. Quit with `:q`, or use `:wq` after edits.
7. Explain the difference between normal, insert, visual, command-line, and search modes in one sentence each.

## Failure / edge case

If `:q` says there are unsaved changes, the learner should choose one:

```vim
:wq   " save and quit
:q!   " discard and quit
```

This failure is intentional: it teaches that Vim distinguishes the buffer from the saved file.

## Checklist / eval

- Each lesson makes one small useful move.
- Each new mode appears only after the learner hits the need for it.
- Escape is practiced repeatedly as the return-to-normal habit.
- The course starts with `vim`, then moves to `vim notes.txt`.
- Quitting appears before serious editing.
- Advanced topics are deferred.

## Cut list / next courses

- Operators and text objects: `dw`, `ciw`, `dap`
- Undo/redo: `u`, `<C-r>`
- Copy/paste: `y`, `p`, registers
- Splits, tabs, buffers, and windows
- Configuration and `.vimrc`
- Plugins and LSP
- MacVim/neovim/editor integrations
