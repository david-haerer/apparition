<p align="center"><h1 align="center">🪄 Apparition 🌀</h1></p>

<p align="center">
<em><a href="https://harrypotter.fandom.com/wiki/Apparition">Apparate</a> through your file system.</em>
</p>

[UX.webm](https://user-images.githubusercontent.com/31665788/217601666-50668871-c91c-424d-aaa7-30da4a25ec67.webm)

<!--autogen-->
## 🪄 Installation

Install the Python package with `pipx` or `pip`.

```bash
pipx install apparition
# or
pip install --user apparition
```

Call the `install` command and add the output to your `~/.bashrc` / `~/.zshrc`.
This creates a shell function called `apparate` that can change the working directory in a safe manner.

```bash
apparition install >> ~/.bashrc
source ~/.bashrc
# or
apparition install >> ~/.zshrc
source ~/.zshrc
```

You can get more information about this step with `apparition install --help`.

```
$ apparition install --help
                                                                                
 Usage: apparition install [OPTIONS]                                            
                                                                                
 🪄 Add the output of this command to your '~/.zshrc'.                          
 You can do this by running 'apparition install >> ~/.zshrc'. Then run 'source  
 ~/.zshrc'.                                                                     
 This creates a shell function called 'apparate' that can change the working    
 directory in a safe manner.                                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

```

## Usage

### ✨ Add or update a destination

Use `apparition set` to add a new destination or update an existing one.

```
$ apparition set --help
                                                                                
 Usage: apparition set [OPTIONS] DESTINATION PATH                               
                                                                                
 ✨ Set a new destination.                                                      
 This command can also be used to update an existing destination.               
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    destination      TEXT  The name of the destination. [default: None]     │
│                             [required]                                       │
│ *    path             PATH  The path to the destination. [default: None]     │
│                             [required]                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 🌀 Apparate to a destination

Use `apparate` to change the working directory.

```
$ apparate --help
                                                                                
 Usage: apparate [OPTIONS] DESTINATION                                          
                                                                                
 🌀 Apparate to the given destination.                                          
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    destination      TEXT  The name of the destination. [default: None]     │
│                             [required]                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### ✍️ Rename a destination

Use `apparition rename` to rename an existing destination.

```
$ apparition rename --help
                                                                                
 Usage: apparition rename [OPTIONS] OLD_NAME NEW_NAME                           
                                                                                
 ✍️ Rename a destination.                                                        
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    old_name      TEXT  Old name of the destination. [default: None]        │
│                          [required]                                          │
│ *    new_name      TEXT  New name of the destination. [default: None]        │
│                          [required]                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### ✔️ Check all destinations

Use `apparition check` to check that the path to each destination is a directory..

```
$ apparition check --help
                                                                                
 Usage: apparition check [OPTIONS]                                              
                                                                                
 ✔️ Check that the path to each destination is a directory.                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 🗑️  Remove a destination

Use `apparition remove` to remove a destination.

```
$ apparition remove --help
                                                                                
 Usage: apparition remove [OPTIONS] DESTINATION                                 
                                                                                
 🗑️ Remove a destination.                                                        
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    destination      TEXT  Name of the destination to remove.               │
│                             [default: None]                                  │
│                             [required]                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### 🔥 Purge all destinations

Use `apparition purge` to delete all destinations.

```
$ apparition purge --help
                                                                                
 Usage: apparition purge [OPTIONS]                                              
                                                                                
 🔥 Remove all destinations.                                                    
 The command asks for confirmation if you are sure.                             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```
<!--/autogen-->

## License

This app is licensed under the [MIT](./LICENSE) license.
