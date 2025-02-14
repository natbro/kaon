[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg?style=flat-square)](https://github.com/tralph3/Steam-Metadata-Editor/blob/master/LICENSE)
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg?style=flat-square)](https://paypal.me/tralph3)

# Steam Metadata Editor

**Edit game titles, launch menus, and more**

---

## Introduction

Steam Metadata Editor is a powerful cross-platform application that lets you edit every single aspect of a Steam App. All the changes are local and are bound to be overwritten by Steam sooner or later. That's why the program keeps track of your changes, and can silently patch them back in if you ask it to do so.

The Editor features an easy-to-use GUI that lets you edit the most important aspects of the applications. If demand is high enough, more features will be added to the GUI. However, if there's anything that you would like to edit that's not possible through the GUI, you can always make changes yourself by editing the JSON.

---

## Usage

When you launch the program, you should see something like this (note that the list of games depends on what you own):

![layout](https://user-images.githubusercontent.com/41462117/224578779-c57cc9a4-4939-4766-8f6c-38491582fa5b.png)

To modify a game, you simply have to click on the one you want, and do your editing. You can use the bar at the top of the list to search for the game you want. In this example, we will edit **Endless Space 2**:

![image](https://user-images.githubusercontent.com/41462117/216202151-8f9776f7-ef7c-4d50-96d7-dcc4590ba5a1.png)

You can see I removed the "Registered" character and removed the "Digital Deluxe Edition" part. I also shortened the **Developer** section.

Once modifications are made, simply click **Save** and restart Steam.

And here are our modifications:

![image](https://user-images.githubusercontent.com/41462117/216202183-3cccc598-4c64-4470-a077-a4e1ebc3cff1.png)

Easy, huh? So what is it useful for?

### You can:

* Remove crap from game titles

* Order your list of games

![image](https://user-images.githubusercontent.com/41462117/216202211-5ad34771-ff71-4a1b-84c1-8b1475eaedc3.png)

* Fix missing executable errors

![image](https://user-images.githubusercontent.com/41462117/216202244-1aea2ccb-9dfd-4de8-8c19-798790127d38.png)

* Create your own launch menus, letting you seamlessly launch multiple modded installations from Steam

![image](https://user-images.githubusercontent.com/41462117/216202278-40ef36a3-a174-4646-a92b-42f5bc11a7d2.png)

* Add missing information like release dates

![image](https://user-images.githubusercontent.com/41462117/216202300-d23a11e2-ef2a-48a4-8074-f4e47868404f.png)

* Any other modification you want through the JSON

* Maybe extra functionality in the future?

---

## How to Use the JSON

For those not familiar with JSON, it's basically a text file that contains data in such a format that it's easily readable by a computer. However, it's also very easy to modify by hand, and you are encouraged to do so.

JSON works with key value pairs. This means that for every **key**, there is a **value**. You can think of this as names for multiple lockers. You want to open a locker called "appinfo", so you ask for the "appinfo" key, and you get whatever is inside.

All of these key value pairs are often referred to as **dictionaries**, and keys can contain other dictionaries too, this is exactly what's going on in the JSON, nested dictionaries.

### Why?

I can't cramp every single thinkable feature into the program, there's just too many possible modifications to do, and you can even store your own data in there if you want to!

For this reason, I let the user see how the data is structured and make the changes they want themselves. This lets non-programmers take a look at the data and maybe even find secret tags that I don't know about that would make good additions.

### How?

Whenever you modify an application (and click save), the data gets stored in the JSON. The first thing you'll see is a key for every appID modified. Find the appID you want, and you'll see it contains two other keys, **original** and **modified**.

The **original** key contains the data of the application as it was before you edited it, it's used to revert the application to its original state. This key should not be tampered with.

The **modified** key contains your modifications. This is the key you want to play with. In here, do whatever you want. Once you are done, simply save the file, open the program and click save. The JSON has been already loaded, and your modifications will be written to Steam.

---

## Silent Patching

Steam likes to overwrite your modifications from time to time. It's certain that at some point, the original data will come back. To try to avoid this (to the best of my ability) I implemented silent patching.

By passing the `-s` or `--silent` argument to the application, it will seamlessly apply your changes without any kind of notice. This is best paired with a script that launches Steam afterward. If it still overwrote your changes, another go should be enough.

---

## FAQ

### What constitutes a valid date?

Dates **must** be entered in YYYY-MM-DD format. A date will be rejected if it's older than 1970 (a.k.a. the start of the universe) or greater than the current date.

### What are the platform checkboxes for?

Entries in the launch menu can be tagged to work for a specific operating system. If an entry has one of these tags set, then that entry will only work if you're using the specified operating system. This feature is mostly useful for Linux users, since they can use Proton, which triggers the Windows entries. If you mark an entry with the Linux checkbox, and you launch the game with Proton, that entry will not be displayed, only Windows ones will work.

### What does the Sort As entry do?

**Sort As** is the name Steam uses to sort your games alphabetically. This entry is automatically filled when you change the name of an app, but can be independently modified. Doing so will let you change the order of apps to whatever you want, so you can have games in a series ordered chronologically instead of by name (by putting a sort of name that alphabetically would give you the desired order). If you snoop around, you'll find that some games already do this.

### Why can't I modify the executable and working directory entries manually?

These entries are special, you can't use absolute paths here, you need to reach your target via relative paths. To avoid confusion and mistakes, use the browse buttons next to the entries to modify them.

---

## Installation

* Linux

Steam Metadata Editor can be downloaded from [Flathub](https://flathub.org/apps/details/io.github.tralph3.Steam_Metadata_Editor). This is the easiest and most straightforward way to install it.

It can also be installed from the [AUR](https://aur.archlinux.org/packages/steam-metadata-editor-git/).

    paru -Syu steam-metadata-editor-git

If you are in an Ubuntu/Debian based distribution, you can download the source code and run the `make_deb.sh` script.

    git clone https://github.com/tralph3/Steam-Metadata-Editor
    cd Steam-Metadata-Editor
    ./make_deb.sh
    sudo apt install ./Steam-Metadata-Editor.deb

You may need to mark it as executable first:

    chmod +x make_deb.sh

Other Linux distributions can download the source code. The program needs Python3.6 or greater with the tk module.

* Windows

Download the source code and install python3.6 or greater. Make sure to install Tk/Tcl with it.

---

## How does it work?

The application is basically an easy way to modify a single file. Located in the folder **appcache** in the Steam installation, there's a file called **appinfo.vdf**. This is a binary file, meaning it's not easily readable, we can only see its bytes. Luckily, I was able to figure out exactly what everything means, with help of course.

### Understanding the layout

This file contains information for every application Steam ever had to download data for. These include all the applications in a user's library, and there may be others thrown in there for no particular reason.

The layout is pretty simple, the first 8 bytes are the header, they specify the version of the vdf file. The rest are the applications.

Applications have a header too, here's what everything means:

**NOTE: The names for these tags and most of this information is taken directly from [steamfiles](https://github.com/leovp/steamfiles) source code. Big thanks to its developer.**

![image](https://user-images.githubusercontent.com/41462117/216202345-dfd555bc-a36b-4b7d-8335-8ffdaca78d88.png)

All of these values are stored in little-endian notation. Right after the last byte in the header, the actual appinfo starts.

Now, this is basically a dictionary of nested dictionaries. Keys have a byte before them that determines the type of data they store. A `0x00` byte determines that it stores a dictionary (that's why the first byte after the last byte in the header is `0x00`), a `0x01` byte means it's a string, and a `0x02` byte means it's a 32-bit integer. There's also `0x07` bytes that represent 64-bit integers, however, I don't think those are used in the appdata. Then you get the name of the key, and another `0x00` byte to separate key from value. There's one last special byte, `0x08`, that determines a dictionary's end. You can see that at the end of every app, there's many of these bytes, signaling the end of many dictionaries.

This is known information, and nothing too complicated. The application just walks through every byte checking what they are and constructs a dictionary out of the data, the same way [steamfiles](https://github.com/leovp/steamfiles) does it (although a bit faster).

### Modifying data

If you try to just change the data to whatever you want, you'll realize that Steam will reject it and revert changes back. Why? The key lies in the `checksum` and `size` tags in the header. Both of these relate to the data directly, and must be updated for Steam to not reject the new data.

**NOTE:** Valve has since modified the header and included an extra checksum that is calculated with the byte data of the app you're modifying. Simply send the bytes through SHA-1, and you should get a valid checksum.

The `size` tag is pretty self-explanatory, it's a 32-bit integer detailing how many bytes of data this application contains, counting from the very next section (`state`) to the very last `0x08` byte.

The `checksum` is of course generated with the data, but how? Simply throwing the bytes at some function won't do the trick. The data needs to be parsed in a specific format, but which? VDF files have a format that we can plainly see in other VDF files.

You see, there's two types of VDF files, binary ones, such as **appinfo.vdf**, and plain text ones, such as **localization.vdf**, located in the same directory. If we take a quick look at **localization.vdf**, we can see how the data is stored, here's a sample:

```
"localization"
{
	"english"
	{
		"store_tags"
		{
			"1663"		"FPS"
			"19"		"Action"
			"1693"		"Classic"
			"5547"		"Arena Shooter"
			"3859"		"Multiplayer"
			"1774"		"Shooter"
			"3878"		"Competitive"
			"6691"		"1990's"
        }
    }
}

```

You can see that everything is enclosed in double quotes, dictionaries break a line and increment indentation, and keys/values are separated by double tabs. And this is the exact format we need to parse **appinfo.vdf** to get the checksum.

**NOTE:** The encoding of the binary data is in UTF-8 for the most part. However, some strings can't be decoded with it. For those cases, I use ISO8859-1 as a fallback, which will decode everything no matter what. This also means that I must use the same encoding when I encode the data back. To signify that I used the ISO8859-1 encoding, I append a `0x06` byte to such strings, which then gets removed when producing checksums or writing data.

Then what do we do exactly? We format all the modified data this way (the function `format_data` takes care of this in my program), and then pass the result through SHA-1, and we get the checksum. *However*, there is one final thing that made me scratch my head for months that I couldn't figure out alone. Some apps have backslashes in their data. These backslashes are usually used for directory paths and stuff like that, and as you may know, backslashes are escape characters.

So... what does this mean to us? It means that I spent months trying to figure out why I could produce valid checksums for some games, while others failed all the time. When generating the checksum, you need to add a second backslash to every single one that appears. That's why in `format_data` I use `replace` to change this: `\\` to this `\\\\`. As the backslash is an escape character, you need another backslash to escape its own special functionality, so there it is, that's the final piece of the puzzle to produce valid checksums.

## Special Thanks

Although I explained it all somewhat gracefully, that doesn't mean I managed to discover it myself sadly. I connected the dots later, but the actual information was provided to me by *Tim Green*, creator of [Steam Edit](https://steamedit.tg-software.com/). My application intends to be a cross-platform and open-source alternative to it, but in no way do I intend to make it obsolete or discredit *Tim*, he has been a great help in the creation of this program, and I'm positive I would not have been able to create it without his help. A big thanks to him.

I'd also like to thank [*Leonid*](https://github.com/leovp) for indirectly aiding me by making the source code of [steamfiles](https://github.com/leovp/steamfiles) freely available to anyone, it has greatly helped me understand how the file worked, and I even borrowed some code.

Finally, thanks to [*xPaw*](https://github.com/xPaw) for documenting an update to the file format that included an extra checksum in [this](https://github.com/SteamDatabase/SteamAppInfo) repo.
