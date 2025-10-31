# file-organizer

A Python CLI tool that automatically organizes messy folders by sorting files into subfolders such as `Images/`, `Documents/`, or `Videos/` based on file type.  

---

## Features

- Sorts files by type (extension-based)
- Automatically creates folders like `Images`, `Documents`, `Videos`, etc.
- Maintains a log file of every file movement
- It can run once or continuously in watch mode to auto sort new files as they appear.

---

## Project Structure

```

file-organizer/
├── organizer.py              # main script
├── config/
│   └── categories.json       # file type config
├── logs/                     # log folder (auto-created)
│   └── activity.log          # log file 
├── requirements.txt          # python dependencies
└── README.md                

```
---

## Usage
```
python organizer.py ~/Downloads
```
