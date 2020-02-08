# NXCompile

Specify XCompose sequences in a simple language and compile them to .XCompose files

## About

Linux/X11 has a feature called [XCompose](https://linux.die.net/man/3/xcompose) which allows you to press a sequence of keys to type a character that doesn't appear on your keyboard. For example, you could press `Compose`, then `c`, then `,` to generate the `ç` character.

The syntax of these compose files is verbose. Enter NXCompile, which lets you specify your key combinations with a simpler and more intuitive syntax, then compile them to the format XCompose prefers.

## Usage

### Input File Syntax

Key sequences are specified in UTF-8 text files. Blank lines, and lines beginning with `#` (symbolizing a comment), are ignored.

The output symbol (or string) must be the first thing on each line. It must be followed by a single Tab character, and the remainder of the line is read as the input characters that should produce that output (after having pressed the `Compose` key).

Examples:

```
ǿ	'/o
≠	/=
Hello World	hw
😉	;)
```

There are more example files in the [examples/](examples/) directory.

If you include any of the glyphs ←↑→↓␈␉␊␍␛␡◆  on the right side of the Tab character, NXCompile will translate them to their respective keyboard keys (with ◆ (U+25C6 BLACK DIAMOND) representing an extra press of the `Compose` key beyond the first press, which is implied for every entry you create). You can disable this behaviour with command-line options, for example if you have a keyboard which can generate the ← symbol and you wish to use that symbol, and not the left arrow key, in a mapping.

### Running NXCompile

You can run `NXCompile -h` to see all options. By default it reads from standard input and writes to standard output.

Running NXCompile on the example from the previous section would produce this output:
```
<Multi_key> <apostrophe> <slash> <o> : "ǿ"
<Multi_key> <slash> <equal> : "≠"
<Multi_key> <h> <w> : "Hello World"
<Multi_key> <semicolon> <parenright> : "😉"
```

### Activating Your Mappings

Place the output of NXCompile into your `~/.XCompose` file. (If you have a curated `.XCompose` file you don't wish to replace, then save the output of NXCompile into a different file, and use the `include` directive.)

Some programs will reflect your changes if you run `setxkbmap`. Others may need to be exited and restarted. You may also need to set the input method in Gnome and KDE programs to XIM (for X Input Method) in order for it to use your customizations.

In any case, you should now be able to press your `Compose` key, followed by any of the sequences you specified, to get your desired symbols.

If you do not have a `Compose` key already mapped, [this page on the ArchLinux Wiki](https://wiki.archlinux.org/index.php/Xorg/Keyboard_configuration#Configuring_compose_key) has some useful information.

### Mapping Considerations

XCompose doesn't allow overlapping input sequences. For example, specifying `Foo` and `Fooo` together is invalid. NXCompile warns you when it finds overlapping mappings. You could change the former mapping to include a trailing space (ie, `Foo␣` with `␣` representing a simple space), this would make them into non-overlapping sequences. (Be careful that your text editor does not strip this trailing space.)

For more considerations, see the [XCompose man page](https://linux.die.net/man/3/xcompose), or the above-linked ArchLinux wiki page.

## Origin

This project is inspired by, can use files for, and borrows some code from, [Recmo/XCompile](https://github.com/Recmo/XCompile). The changes I made to it quickly left the realm of "patch" and became their own project. Hence, "NXCompile" for "New XCompile". Nonetheless, this still owes its lineage to Recmo's project. Thanks Recmo for the useful tool and the inspiration!

### Differences from XCompile

Advantages over XCompile:

* Written in Python 3
    * Python 2 is no longer supported as of January 1, 2020
* Support any keyboard key which can generate its own glyph
    * List of supported keys is taken from the X standard, via `keysymdefs.h`
* Allow disabling treatment of ←↑→↓ symbols as the keyboard arrow keys
    * In case you have a keyboard that can output those as glyphs
* Treat ␈␉␊␍␛␡◆ symbols as keyboard keys (but allow disabling that behaviour)
* More precise error messages
    * Give the file name and location of syntax problems
* Option to suppress non-sequence lines (comments and blank lines) from being copied to XCompose file
* Option to add source file names as comments to XCompose file
* Support `"` and `\` in target text

Disadvantages compared to XCompile:

* Key names are in a separate Python source file
    * The file `keysyms.py` must be in your python library path, or in the same directory as `NXCompile` (but you can symlink NXCompile to wherever you like)

## Possible Future Improvements

* Support for dead keys
    * What would this look like in the source file?
* Support for other input and output encodings besides UTF-8
* Proper packaging as a `pip` module
    * To keep the end user from having to worry about the location of `keysyms.py`
