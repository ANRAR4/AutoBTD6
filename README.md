# Introduction

The scripts contained in this repository allow you to automatically play any gamemode on any map in Bloons Tower Defence 6.
<br>
This can be used for automatically farming monkey money, player xp, tower xp, medals, achievements or collection event rewards.
<br>
Additionally the scripts allow you to record your own playthroughs to a textual description which can be automatically replayed afterwards.


The scripts have only been tested on Windows.

The config files (list of maps, monkey upgrade costs) are currently set up for **Bloons TD6 v47.0**.
<br>
If Ninja Kiwi releases a new major version of Bloons TD6 and the repository is outdated you can easily update it yourself.
<br>
For more information refer to [supporting new versions of Bloons TD6](#supporting-new-versions-of-bloons-td6).

**Please be aware Ninja Kiwi doesn't support modding or use of external scripts for automated farming and may flag or ban accounts as a result when using this or similar scripts (although this hasn't happend to any of my accounts yet).**

# Table of contents
1. [How the replay of a playthrough works](#how-the-replay-of-a-playthrough-works)<br>
2. [Usage / Modes of operation](#usage--modes-of-operation)<br>
   1. [Playing a specific playthrough](#file---playing-a-specific-playthrough)<br>
   2. [Playing a random map](#random---playing-a-random-map)<br>
   3. [Play a map with increased collection event rewards](#chase---play-a-map-with-increased-collection-event-rewards)<br>
   4. [Play playthroughs that grant missing achievements](#achievements---play-playthroughs-that-grant-missing-achievements)<br>
   5. [Playing playthroughs that grant missing medals](#missing---play-playthroughs-that-grant-missing-medals)<br>
   6. [Play the most efficient maps for player xp farming](#xp---play-the-most-efficient-maps-for-player-xp-farming)<br>
   7. [Play the most efficient maps for monkey money farming](#mm---play-the-most-efficient-maps-for-monkey-money-farming)<br>
   8. [Validate playthroughs](#validate---validate-playthroughs)<br>
   9. [Determine cost of each monkey, upgrade and hero](#costs---determine-cost-of-each-monkey-upgrade-and-hero)<br>
   10. [Gamemode parameter](#gamemode-parameter)
   11. [Category parameter](#category-parameter)
   12. [Map parameter](#map-parameter)
   13. [Hero parameter](#hero-parameter)
   14. [Optional arguments](#flags--optional-arguments)<br>
   15. [Examples](#examples)<br>
   16. [Pausing / Stopping execution](#pausing--stopping-execution)<br>
3. [Requirements / Installation](#requirements)<br>
   1. [Installation](#installation)<br>
   2. [Ingame settings](#ingame-settings)<br>
   3. [Other prerequisites](#other-prerequisites)
4. [Supported maps](#currently-supported-maps)<br>
5. [Recording playthroughs](#recording-playthroughs)<br>
   1. [Contributing playthroughs](#contributing-playthroughs)<br>
   2. [Beast Handler](#beast-handler)<br>
6. [Additional scripts](#additional-scripts)<br>
7. [Supported resolutions](#supported-resolutions)<br>
8. [Supporting new collection events](#supporting-new-collection-events)<br>
9. [Supporting new versions of Bloons TD6](#supporting-new-versions-of-bloons-td6)<br>
   1.  [Adding new maps](#adding-new-maps)<br>
   2.  [Incorporating balance changes in regards to tower/upgrade cost](#incorporating-balance-changes-in-regards-to-towerupgrade-cost)<br>
   3.  [Adding new towers](#adding-new-towers)<br>
   4.  [Adding new heros](#adding-new-heros)<br>
   5.  [Major GUI changes](#major-gui-changes)<br>
10. [Known issues](#known-issues)<br>


# How the replay of a playthrough works

Playthroughs consist of actions like placing or upgrading a monkey, each associated with a specific cost.
The replay of a playthrough works by periodically taking screenshots of BTD6 to determine what menu you are in or how much money you have available. If there is more money available than required for the next action in the playthrough it performs the corresponding action. This repeats until the game is won, lost or all actions have been performed.

Outside of a playthrough the script is able to navigate through BTD6 e. g. to select a hero or map and gamemode.

# Usage / Modes of operation

The general command structure is `py replay.py <mode> <mode arguments...> <flags>`

## `file` - Playing a specific playthrough

Usage: `py replay.py file <filename> [gamemode] [continue <(int start|-)> [until (int end)]] <flags>`

Replays the specified file. Navigates to ingame if continue is not set.
<br>
If `filename` contains `/` or `\` `filename` is used as the path. otherwise the script lookes for `filename` in `own_playthroughs`, then in `playthroughs`
<br>
<br>
`gamemode` can be specified to overwrite the gamemode in the files title. (e. g. `py replay.py file dark_castle#chimps#2560x1440#noMK#noLL.btd6 medium -nomk` to play dark castle on medium using the recorded playthrough for chimps)
<br>
if continue is set:
- it is assumed you are already in the correct game
- the script starts with instruction start (0 for first instruction)
- if `start` = `-` all instructions are executed before the game is started
- if `until` is specified the script ends before instruction `end` (e. g. start=0, end=1 -> only first instruction is executed)
- continue is mostly useful for debugging playthroughs

flag `-r` only works if `continue` is not specified


## `random` - Playing a random map

Usage: `py replay.py random [category] [gamemode] <flags>`

Plays a random game from all available playthroughs (which fullfill the category and gamemode requirement if specified)
<br>
Combined with the `-r` flag a playthrough is selected at random each iteration.

## `chase` - Play a map with increased collection event rewards

Usage: `py replay.py chase <event> [category] [gamemode] <flags>`

Chases increased rewards for the specified event. Currently supported events are: 
- `totem`: Totem collection event
- `halloween`: Halloween collection event
- `present`: Christmas collection event
- `easter`: Easter collection event
- `independence`: Independence day collection event
- `birthday`: BTD6 Birthday collection event
  
If category is not provided it finds the map with increased rewards in expert category and if a playthrough is available plays it. If not it searches the advanced category and so on.
<br>
If category is provided only said category is searched.

Category and gamemode can be specified to restrict the considered playthroughs.
<br>
If there are no suitable playthroughs available the script exits.

## `achievements` - Play playthroughs that grant missing achievements

To be implemented

e. g. `so spiiicey ninja kiwi` - `beat spice islands on alternate bloons rounds with only land towers`

## `missing` - Play playthroughs that grant missing medals

To be implemented

## `xp` - Play the most efficient maps for player xp farming

Usage: `py replay.py xp [int n=1]`

Plays a random playthrough out of the `n` most efficient (in terms of xp/hour) playthroughs.

Efficiency is calculated using the average of `win_times` in `playthrough_stats.json`. This means new playthroughs need to be played at least once to get considered.

For some context: currently the most efficient of the included playthroughs is dark castle on chimps which will earn you about 800k XP/hour(given your game doesn't lag)

## `mm` - Play the most efficient maps for monkey money farming

Usage: `py replay.py mm [int n=1]`

Plays a random playthrough out of the `n` most efficient (in terms of monkey money/hour) playthroughs.

Efficiency is calculated using the average of `win_times` in `playthrough_stats.json`. This means new playthroughs need to be played at least once to get considered.

For some context: currently the most efficient of the included playthroughs is bloody puddles on hard which will earn you about 760 Monkey money/hour (given your game doesn't lag) (836 Monkey Money/Hour if you have `mo' monkey money` unlocked).

## `validate` - Validate playthroughs

Usage: `py replay.py validate file <filename>` or `py replay.py validate all [category] [gamemode]`

Validates a or multiple playthroughs in regards to monkey positions by setting them up in sandbox mode and checking if all actions have been performed correctly. Validation is restricted to your screens resolution, different resolutions must be validated seperately.

When run as `py replay.py validate all` all playthroughs will be validated. When appending the `-nv` flag only non validated playthroughs will be validated!

**This mode requires monkey knowledge to be disabled!**

If used with `file` parameter:
Validates playthrough `filename`.

If used with `all` parameter:
Validates all playthroughs which fullfill the category and gamemode requirement if specified.

`-r` flag has no effect for this mode.

## `costs` - Determine cost of each monkey, upgrade and hero

Usage: `py replay.py costs [+heros]`

Determines the cost of each monkey and each upgrade of each monkey. Additionally determines the base cost of each hero if `+hero` is specified.

If `+hero` is set all heros will be tested.

**This mode requires monkey knowledge to be disabled!**<br>
**This mode requires all upgrades to be unlocked!**

Can be used after an update to BTD6 to automatically update `towers.json`.

Creates a backup of the old `towers.json` file under `towers_backup.json`.


## `gamemode` parameter

The `gamemode` parameter can be one of the following:

- `easy` (for standard in easy difficulty)
- `primary_only`
- `deflation`
- `medium` (for standard in medium difficulty)
- `military_only`
- `reverse`
- `apopalypse`
- `hard` (for standard in hard difficulty)
- `magic_monkeys_only`
- `double_hp_moabs`
- `half_cash`
- `alternate_bloons_rounds`
- `impoppable`
- `chimps`

## `category` parameter

The `category` parameter can be one of the following:
- `beginner`
- `intermediate`
- `advanced`
- `expert`

## `map` parameter

The `map` parameter can be one of the following:
- `monkey_meadow`
- `tree_stump`
- `town_center`
- `tinkerton`
- `middle_of_the_road`
- `one_two_tree`
- `scrapyard`
- `the_cabin`
- `resort`
- `skates`
- `lotus_island`
- `candy_falls`
- `winter_park`
- `carved`
- `park_path`
- `alpine_run`
- `frozen_over`
- `in_the_loop`
- `cubism`
- `four_circles`
- `hedge`
- `end_of_the_road`
- `logs`
- `luminous_cove`
- `sulfur_springs`
- `water_park`
- `polyphemus`
- `covered_garden`
- `quarry`
- `quiet_street`
- `bloonarius prime`
- `balance`
- `encrypted`
- `bazaar`
- `adoras_temple`
- `spring_spring`
- `kartsndarts`
- `moon_landing`
- `haunted`
- `downstream`
- `firing_range`
- `cracked`
- `streambed`
- `chutes`
- `rake`
- `spice_islands`
- `enchanted_glade`
- `last_resort`
- `ancient_portal`
- `castle_revenge`
- `dark_path`
- `erosion`
- `midnight_mansion`
- `sunken_columns`
- `x_factor`
- `mesa`
- `geared`
- `spillway`
- `cargo`
- `pats_pond`
- `peninsula`
- `high_finance`
- `another_brick`
- `off_the_coast`
- `cornfield`
- `underground`
- `glacial_trail`
- `dark_dungeons`
- `sanctuary`
- `ravine`
- `flooded_valley`
- `infernal`
- `bloody_puddles`
- `workshop`
- `quad`
- `dark_castle`
- `muddy_puddles`
- `ouch`

# `hero` parameter

The `hero` parameter can be one of the following:
- `quincy`
- `gwendolin`
- `striker_jones`
- `obyn_greenfoot`
- `rosalia`
- `captain_churchill`
- `benjamin`
- `ezili`
- `pat_fusty`
- `adora`
- `admiral_brickell`
- `etienne`
- `sauda`
- `psi`
- `geraldo`

the hero `corvus` is currently not supported

## Flags / Optional arguments

<table>
<tr>
<th>Flag</th>
<th>Description</th>
</tr>
<tr>
<td>-r</td>
<td>repeat objective indefinitely (e. g. `py replay.py file dark_castle#chimps#2560x1440#noMK#noLL.btd6 -r` to repeatedly play the map dark castle on chimps)</td>
</tr>
<tr>
<td>-ns</td>
<td>disable stats logging. if not disabled the number and duration of playthroughs will be logged to `playthrough_stats.json`. Some modes use this information to determine the most efficient playthrough for farming. Disabling is mainly for testing purposes.</td>
</tr>
<tr>
<td>-mk</td>
<td>consider playthroughs with arbitrary monkey knowledge as a requirement. also adjust monkey pricing according to your monkey knowledge (`userconfig.json`)</td>
</tr>
<tr>
<td>-nomk</td>
<td>ignore playthroughs with monkey knowledge as a requirement. also don't adjust monkey pricing according to your monkey knowledge (`userconfig.json`)</td>
</tr>
<tr>
<td>-nv</td>
<td>include non validated playthroughs in selection. not recommended as non validated playthroughs might not work due to invalid monkey positions.</td>
</tr>
<tr>
<td>-l</td>
<td>list all found playthroughs and exit. can only be used with modes other than `file`</td>
</tr>
</table>

## Examples

Play dark castle on chimps. Pricing in chimps is identical with and without monkey knowledge: 
<br>
`py replay.py file dark_castle#chimps#2560x1440#noMK#noLL.btd6 -mk`


Indefinitely farm XP on the 3 most efficient maps:
<br>
`py replay.py xp 3 -mk -r`


Indefinitely farm XP on the 3 most efficient maps that don't require any monkey knowledge:
<br>
`py replay.py xp 3 -nomk -r`

Indefinitely farm monkey money on the most efficient map:
<br>
`py replay.py mm -mk -r`


Indefinitely farm increased totem collection event rewards on the most rewarding maps even considering playthroughs that aren't reproducable without monkey knowledge:
<br>
`py replay.py chase totem -r -mk`


Play a random map on double hp moabs in beginner category that doesn't require any monkey knowledge:
<br>
`py replay.py random beginner double_hp_maobs -nomk`

Validate all unvalidated playthroughs in category beginner:
<br>
`py replay.py validate all beginner -nomk -nv`


Validate playthrough file `dark_castle#chimps#2560x1440#noMK#noLL.btd6`:
<br>
`py replay.py validate file dark_castle#chimps#2560x1440#noMK#noLL.btd6 -nomk`

## Pausing / Stopping execution

While `ctrl` is pressed or Bloons TD6 is not your active window the execution of the script will be paused.

Furthermore you can order the script to exit after finishing the current playthrough by pressing `ctrl` and `space` while in Bloons TD6.

You can immediately stop execution by sending SIGINT to the script (pressing `ctrl` + `c` while in the command window the script is running in).

# Requirements

## Installation
To run the scripts you must have Python 3 (3.5 or higher) ([www.python.org](https://www.python.org)) installed. 
<br>
Aditionally all pip packages listed in `requirements.txt` must be installed.
<br>
This can be achieved by running:
<br>
`pip install -r requirements.txt --user`

The required packages also include Tensorflow which requires additional DLLs (Microsoft C++ Redistributable for Visual Studio [...]) to run. When running replay.py for the first time Tensorflow will output an error and list what dlls are missing and where they can be downloaded from.

Additionally the python `ahk` library requires AutoHotkey ([www.autohotkey.com](https://www.autohotkey.com)) to be installed.

For some reason keystrokes send using `PyAutoGUI` don't get registered by BTD6, thats why the script also requires the `ahk` library even if `PyAutoGUI` theoretically provides the required functions.

## Ingame Settings

Additionally some specific ingame settings are required:

- setting your ingame language to english (under settings -> language)
- BTD6 running at your screens native resolution and on your primary screen
- disabling any big/small tower or bloon effects (under settings -> extras)(they get unlocked by specific achievements, if not unlocked they are disabled)
- in the escape menu while ingame:
  - placement mode: drag & drop
  - game hints: off
  - auto start: on (optional but recommended)

### Keybinds
If you changed your keybinds for placing or upgrading towers, retargeting, monkey special or selling they should be reset or you need to specify them inside `keybinds.json`.
Latter requires the python keyboard library names of the corresponding keys or their scancode in categories "monkeys", "path" and "recording". Scancodes are the safer option. You can find out the scancodes/names of keys by running `log_keypresses.py`. This will print both values when pressing a key.

The entries in category "others" require the AHK Keynames.

## Other prerequisites

When using the script in a mode other than `file` configurating `userconfig.json` is required so the script can tell which playthroughs you can play.
The most importants segments are `heros` where you can specify whether you have a specific hero unlocked (`true` = unlocked, `false` = not unlocked), `unlocked_maps` where you can specify whether you have a specific map unlocked (`true` = unlocked, `false` = not unlocked) and `medals` where you can specify whether you have a specific medal for a specific map already (`true` = medal acquired, `false` = medal not acquired). The `medals` section will be updated automatically when the script gets a new medal.

The default configuration has all maps and heros unlocked.

### Mermonkey

Due to not having a default hotkey assigned using the mermonkey requires setting its hotkey to `o` or changing the hotkey in `keybinds.json`.

**Additionally you should make sure to move or ideally disable popups that may appear in the lower right corner of the screen (e. g. from Steam) as they might interfere with the script and cause you to lose playthroughs.**

# Currently supported maps

The following table lists which gamemodes for which maps have recorded playthroughs available.
<br>
By hovering over a listing you can see what monkeys (and upgrades) are required for the playthrough.
<br>
By clicking a listing you are redirected to the corresponding file to view it or copy its name for replaying.
<br>
<br>
Listings follow the following format:
<br>
Format: `status, hero, comments/flags, native: <playthroughs native resolution>, tested: <resolutions the playthrough has been tested for>`

Status:
- supported: playthrough works with Monkey Knowledge disabled
- with MK: playthrough uses arbitrary Monkey Knowledge, not necessarily reproducable

Hero: hero used for playthrough
- `Heroname`: hero `Heroname` required
- `-`: no hero used

Flags:
<table>
<tr>
<th>Flag</th>
<th>Meaning</th>
</tr>
<tr>
<td>*</td>
<td>lifes lost</td>
</tr>
<tr>
<td>(*)</td>
<td>lifes lost without monkey knowledge, no lifes lost with specific monkey knowledge (mainly mana lives and free roadspikes)</td>
</tr>
</table>

An _italic_ listing means the corresponding playthrough is derived from a playthrough for an harder gamemode on the same map.

<div id="supported_maps">
<table border=1 style="border-collapse: collapse">
	<tr>
		<th>Map</th>
		<th>Category</th>
		<th>Easy</th>
		<th>Primary only</th>
		<th>Deflation</th>
		<th>Medium</th>
		<th>Military only</th>
		<th>Reverse</th>
		<th>Apopalypse</th>
		<th>Hard</th>
		<th>Magic monkeys only</th>
		<th>Double HP moabs</th>
		<th>Half cash</th>
		<th>Alternate bloons rounds</th>
		<th>Impoppable</th>
		<th>C.H.I.M.P.S</th>
		<th>Comment</th>
	</tr>
	<tr style="border-top: 2px solid white">
	<th>Monkey meadow</th>
	<td rowspan=23>beginner</th>
		<td><a href="playthroughs%2Fmonkey_meadow%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: druid(1-3-0), heli(5-2-0), ice(2-0-5), dart(0-2-5)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23double_hp_moabs%231920x1080%23noMK%23noLL.btd6"title="required monkeys: heli(5-2-0), ace(4-0-0)"><i>supported, Sauda, military monkeys only, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23easy%232560x1440%23noMK%23noLL.btd6"title="required monkeys: engineer(4-2-0)">supported, Sauda, engineer only, support monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fmonkey_meadow%23half_cash%231920x1080%23noMK.btd6"title="required monkeys: tack(0-2-2), boomerang(4-0-2), bomb(0-3-0), dart(0-2-5), ice(2-0-0)"><i>supported, Sauda, primary monkeys only, *, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: engineer(4-2-5)"><i>supported, Etienne, engineer only, support monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-5), wizard(5-0-2), druid(1-5-0)"><i>supported, Captain_churchill, magic monkeys only, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23half_cash%231920x1080%23noMK.btd6"title="required monkeys: tack(0-2-2), boomerang(4-0-2), bomb(0-3-0), dart(0-2-5), ice(2-0-0)"><i>supported, Sauda, primary monkeys only, *, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23deflation%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, Sauda, ninja only, magic monkeys only, native: 2560x1440, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: druid(1-3-0), heli(5-2-0), ice(2-0-5), dart(0-2-5)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23double_hp_moabs%231920x1080%23noMK%23noLL.btd6"title="required monkeys: heli(5-2-0), ace(4-0-0)"><i>supported, Sauda, military monkeys only, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23half_cash%231920x1080%23noMK.btd6"title="required monkeys: tack(0-2-2), boomerang(4-0-2), bomb(0-3-0), dart(0-2-5), ice(2-0-0)"><i>supported, Sauda, primary monkeys only, *, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: engineer(4-2-5)"><i>supported, Etienne, engineer only, support monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-5), wizard(5-0-2), druid(1-5-0)"><i>supported, Captain_churchill, magic monkeys only, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23double_hp_moabs%231920x1080%23noMK%23noLL.btd6"title="required monkeys: heli(5-2-0), ace(4-0-0)"><i>supported, Sauda, military monkeys only, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23reverse%231920x1080%23noMK%23noLLwMK.btd6"title="required monkeys: dart(0-2-5)">supported, Obyn_greenfoot, dart only, primary monkeys only, (*), native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23apopalypse%231920x1080%23noMK%23noLL.btd6"title="required monkeys: druid(1-3-0), wizard(4-0-3)">supported, Obyn_greenfoot, magic monkeys only, native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: druid(1-3-0), heli(5-2-0), ice(2-0-5), dart(0-2-5)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23double_hp_moabs%231920x1080%23noMK%23noLL.btd6"title="required monkeys: heli(5-2-0), ace(4-0-0)"><i>supported, Sauda, military monkeys only, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23half_cash%231920x1080%23noMK.btd6"title="required monkeys: tack(0-2-2), boomerang(4-0-2), bomb(0-3-0), dart(0-2-5), ice(2-0-0)"><i>supported, Sauda, primary monkeys only, *, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fmonkey_meadow%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: engineer(4-2-5)">supported, Etienne, engineer only, support monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fmonkey_meadow%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-5), wizard(5-0-2), druid(1-5-0)"><i>supported, Captain_churchill, magic monkeys only, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-5), wizard(5-0-2), druid(1-5-0)"><i>supported, Captain_churchill, magic monkeys only, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23double_hp_moabs%231920x1080%23noMK%23noLL.btd6"title="required monkeys: heli(5-2-0), ace(4-0-0)">supported, Sauda, military monkeys only, native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23half_cash%231920x1080%23noMK.btd6"title="required monkeys: tack(0-2-2), boomerang(4-0-2), bomb(0-3-0), dart(0-2-5), ice(2-0-0)">supported, Sauda, primary monkeys only, *, native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23alternate_bloons_rounds%231920x1080%23noMK%23noLL.btd6"title="required monkeys: druid(1-3-0), engineer(0-3-0), heli(4-2-0), mortar(0-2-4)">supported, Sauda, native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-5), wizard(5-0-2), druid(1-5-0)">supported, Captain_churchill, magic monkeys only, native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fmonkey_meadow%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: druid(1-3-0), heli(5-2-0), ice(2-0-5), dart(0-2-5)">supported, Sauda, native: 1920x1080, tested for: 1920x1080</a></td>
		<td></td>
	</tr>
	<tr>
	<th>In the loop</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Middle of the road</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Tinkerton</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Tree stump</th>
		<td><a href="playthroughs%2Ftree_stump%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Town center</th>
		<td><a href="playthroughs%2Ftown_center%23easy%232560x1440%23noMK%23noLL.btd6"title="required monkeys: boomerang(4-0-2), wizard(0-2-4), bomb(2-4-0)">supported, -, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>One two tree</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Scrapyard</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>The cabin</th>
		<td><a href="playthroughs%2Fthe_cabin%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Resort</th>
		<td><a href="playthroughs%2Fresort%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fresort%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), ninja(2-0-4)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fresort%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), ninja(2-0-4)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fresort%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), ninja(2-0-4)">supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Skates</th>
		<td><a href="playthroughs%2Fskates%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Lotus island</th>
		<td><a href="playthroughs%2Flotus_island%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Candy falls</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcandy_falls%23alternate_bloons_rounds%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(5-2-0), village(1-2-0), sniper(4-0-2), heli(4-0-2)">supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Winter park</th>
		<td><a href="playthroughs%2Fwinter_park%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Carved</th>
		<td><a href="playthroughs%2Fcarved%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Park path</th>
		<td><a href="playthroughs%2Fpark_path%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), ninja(2-0-4), heli(3-0-2), druid(3-1-0)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fpark_path%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), ninja(2-0-4), heli(3-0-2), druid(3-1-0)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fpark_path%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), ninja(2-0-4), heli(3-0-2), druid(3-1-0)">supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Alpine run</th>
		<td><a href="playthroughs%2Falpine_run%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Frozen over</th>
		<td><a href="playthroughs%2Ffrozen_over%23double_hp_moabs%232560x1440%23noMK.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), heli(4-0-3), buccaneer(5-2-0)"><i>supported, Etienne, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Ffrozen_over%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(1-2-0), heli(3-0-2), sniper(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Ffrozen_over%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: ninja(4-0-4), druid(3-0-2), super(3-2-0), wizard(0-2-5)"><i>supported, Etienne, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Ffrozen_over%23double_hp_moabs%232560x1440%23noMK.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), heli(4-0-3), buccaneer(5-2-0)"><i>supported, Etienne, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Ffrozen_over%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(1-2-0), heli(3-0-2), sniper(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Ffrozen_over%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: ninja(4-0-4), druid(3-0-2), super(3-2-0), wizard(0-2-5)"><i>supported, Etienne, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Ffrozen_over%23apopalypse%232560x1440%23noMK.btd6"title="required monkeys: buccaneer(4-4-0), village(1-2-0), heli(3-0-3)">supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Ffrozen_over%23double_hp_moabs%232560x1440%23noMK.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), heli(4-0-3), buccaneer(5-2-0)"><i>supported, Etienne, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Ffrozen_over%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(1-2-0), heli(3-0-2), sniper(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Ffrozen_over%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: ninja(4-0-4), druid(3-0-2), super(3-2-0), wizard(0-2-5)"><i>supported, Etienne, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Ffrozen_over%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: ninja(4-0-4), druid(3-0-2), super(3-2-0), wizard(0-2-5)">supported, Etienne, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Ffrozen_over%23double_hp_moabs%232560x1440%23noMK.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), heli(4-0-3), buccaneer(5-2-0)">supported, Etienne, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Ffrozen_over%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(1-2-0), heli(3-0-2), sniper(4-0-2)">supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Cubism</th>
		<td><a href="playthroughs%2Fcubism%23double_hp_moabs%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), ninja(2-0-4), heli(4-0-3)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcubism%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(4-2-0), sniper(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcubism%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: wizard(0-4-4), druid(4-0-2), ninja(4-0-4), alchemist(0-2-5)"><i>supported, -, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcubism%23double_hp_moabs%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), ninja(2-0-4), heli(4-0-3)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcubism%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(4-2-0), sniper(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcubism%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: wizard(0-4-4), druid(4-0-2), ninja(4-0-4), alchemist(0-2-5)"><i>supported, -, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcubism%23apopalypse%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), village(0-2-0), bomb(2-4-0), heli(2-0-3), sniper(4-0-2)">supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Fcubism%23double_hp_moabs%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), ninja(2-0-4), heli(4-0-3)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcubism%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(4-2-0), sniper(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcubism%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: wizard(0-4-4), druid(4-0-2), ninja(4-0-4), alchemist(0-2-5)"><i>supported, -, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fcubism%23magic_monkeys_only%232560x1440%23noMK.btd6"title="required monkeys: wizard(0-4-4), druid(4-0-2), ninja(4-0-4), alchemist(0-2-5)">supported, -, magic monkeys only, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Fcubism%23double_hp_moabs%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), ninja(2-0-4), heli(4-0-3)">supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Fcubism%23half_cash%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), buccaneer(4-2-0), village(4-2-0), sniper(4-0-2)">supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Four circles</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Hedge</th>
		<td><a href="playthroughs%2Fhedge%23easy%232560x1440%23noMK%23ninjaOnly%23noLL.btd6"title="required monkeys: ninja(4-0-4)">supported, -, ninja only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>End of the road</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Logs</th>
		<td><a href="playthroughs%2Flogs%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-2-0), ninja(0-0-1), heli(4-0-3), ice(2-0-5), glue(5-0-2)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Flogs%23easy%232560x1440%23noMK%23buccaneerOnly%23noLL.btd6"title="required monkeys: buccaneer(0-4-2)">supported, -, buccaneer only, military monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Flogs%23impoppable%232560x1440%23noMK%23noLL.btd6"title="required monkeys: druid(2-5-0), village(5-2-0), dart(0-2-5), alchemist(4-0-2), tack(5-0-2)"><i>supported, Quincy, native: 2560x1440</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Flogs%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-2-0), ninja(0-0-1), heli(4-0-3), ice(2-0-5), glue(5-0-2)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Flogs%23impoppable%232560x1440%23noMK%23noLL.btd6"title="required monkeys: druid(2-5-0), village(5-2-0), dart(0-2-5), alchemist(4-0-2), tack(5-0-2)"><i>supported, Quincy, native: 2560x1440</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Flogs%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-2-0), ninja(0-0-1), heli(4-0-3), ice(2-0-5), glue(5-0-2)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Flogs%23impoppable%232560x1440%23noMK%23noLL.btd6"title="required monkeys: druid(2-5-0), village(5-2-0), dart(0-2-5), alchemist(4-0-2), tack(5-0-2)"><i>supported, Quincy, native: 2560x1440</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Flogs%23impoppable%232560x1440%23noMK%23noLL.btd6"title="required monkeys: druid(2-5-0), village(5-2-0), dart(0-2-5), alchemist(4-0-2), tack(5-0-2)">supported, Quincy, native: 2560x1440</a></td>
		<td><a href="playthroughs%2Flogs%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-2-0), ninja(0-0-1), heli(4-0-3), ice(2-0-5), glue(5-0-2)">supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
	</tr>
	<tr style="border-top: 2px solid white">
	<th>Luminous Cove</th>
	<td rowspan=23>intermediate</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Sulfur springs</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Water park</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Polyphemus</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Covered garden</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td>positions and monkeys not always accessible (2)</td>
	</tr>
	<tr>
	<th>Quarry</th>
		<td><a href="playthroughs%2Fquarry%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fquarry%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fquarry%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fquarry%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)">supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Quiet street</th>
		<td><a href="playthroughs%2Fquiet_street%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-2-5), super(3-2-0)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fquiet_street%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-2-5), super(3-2-0)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fquiet_street%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-2-5), super(3-2-0)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fquiet_street%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-2-5), super(3-2-0)">supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Bloonarius prime</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Balance</th>
		<td><a href="playthroughs%2Fbalance%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: alchemist(3-2-0), ninja(2-0-4), wizard(0-2-5)"><i>supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fbalance%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: alchemist(3-2-0), ninja(2-0-4), wizard(0-2-5)"><i>supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fbalance%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: alchemist(3-2-0), ninja(2-0-4), wizard(0-2-5)"><i>supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fbalance%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: alchemist(3-2-0), ninja(2-0-4), wizard(0-2-5)">supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Encrypted</th>
		<td><a href="playthroughs%2Fencrypted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5), ninja(2-0-4)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fencrypted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5), ninja(2-0-4)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fencrypted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5), ninja(2-0-4)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fencrypted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5), ninja(2-0-4)">supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Bazaar</th>
		<td><a href="playthroughs%2Fbazaar%23medium%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-4), ninja(2-0-4), druid(4-0-2)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fbazaar%23medium%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-4), ninja(2-0-4), druid(4-0-2)">supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Adora's temple</th>
		<td><a href="playthroughs%2Fadoras_temple%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5)"><i>supported, Sauda, wizard only, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fadoras_temple%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5)"><i>supported, Sauda, wizard only, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fadoras_temple%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5)"><i>supported, Sauda, wizard only, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fadoras_temple%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(4-3-5)">supported, Sauda, wizard only, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Spring spring</th>
		<td><a href="playthroughs%2Fspring_spring%23medium%232560x1440%23noMK%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-3), village(0-2-0)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fspring_spring%23medium%232560x1440%23noMK%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-3), village(0-2-0)">supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Kartsndarts</th>
		<td><a href="playthroughs%2Fkartsndarts%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(0-2-0), sniper(4-0-2)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fkartsndarts%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(0-2-0), sniper(4-0-2)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fkartsndarts%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(0-2-0), sniper(4-0-2)">supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Moon landing</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Haunted</th>
		<td><a href="playthroughs%2Fhaunted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: super(3-0-2), alchemist(4-2-0)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fhaunted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: super(3-0-2), alchemist(4-2-0)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fhaunted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: super(3-0-2), alchemist(4-2-0)"><i>supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fhaunted%23magic_monkeys_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: super(3-0-2), alchemist(4-2-0)">supported, Sauda, magic monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Downstream</th>
		<td><a href="playthroughs%2Fdownstream%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fdownstream%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fdownstream%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fdownstream%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)">supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Firing range</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Cracked</th>
		<td><a href="playthroughs%2Fcracked%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(0-2-5), super(3-0-2)"><i>supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcracked%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(0-2-5), super(3-0-2)"><i>supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcracked%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(0-2-5), super(3-0-2)"><i>supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fcracked%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(0-2-5), super(3-0-2)">supported, Sauda, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Streambed</th>
		<td><a href="playthroughs%2Fstreambed%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fstreambed%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fstreambed%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)"><i>supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fstreambed%23magic_monkeys_only%232560x1440%23noMK%23noLL.btd6"title="required monkeys: wizard(4-2-5)">supported, Sauda, wizard only, magic monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Chutes</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Rake</th>
		<td><a href="playthroughs%2Frake%23hard%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(2-2-0), buccaneer(4-2-0), sniper(4-0-2)"><i>supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Frake%23hard%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(2-2-0), buccaneer(4-2-0), sniper(4-0-2)"><i>supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Frake%23hard%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(2-2-0), buccaneer(4-2-0), sniper(4-0-2)">supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Spice islands</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fspice_islands%23alternate_bloons_rounds%232560x1440%23noMK%23noWaterTowers.btd6"title="required monkeys: tack(4-2-2), sniper(4-1-2), heli(4-0-4), ninja(2-0-4), village(2-2-0), druid(3-0-2)">supported, Sauda, *, no water towers(achievement), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr style="border-top: 2px solid white">
	<th>Enchanted Glade</th>
	<td rowspan=20>advanced</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Last Resort</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Ancient Portal</th>
		<td><a href="playthroughs%2Fancient_portal%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: tack(5-0-2), dart(2-0-5)"><i>with MK, Sauda, primary monkeys only, (*), native: 2560x1440</i></a></td>
		<td><a href="playthroughs%2Fancient_portal%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: tack(5-0-2), dart(2-0-5)"><i>with MK, Sauda, primary monkeys only, (*), native: 2560x1440</i></a></td>
		<td></td>
		<td><a href="playthroughs%2Fancient_portal%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: tack(5-0-2), dart(2-0-5)"><i>with MK, Sauda, primary monkeys only, (*), native: 2560x1440</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fancient_portal%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: tack(5-0-2), dart(2-0-5)">with MK, Sauda, primary monkeys only, (*), native: 2560x1440</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Castle revenge</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Dark path</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Erosion</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Midnight mansion</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Sunken columns</th>
		<td><a href="playthroughs%2Fsunken_columns%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-4), sniper(4-0-2), tack(4-0-2), buccaneer(4-2-0)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fsunken_columns%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(0-2-4), heli(4-0-3), sniper(4-0-2), village(2-2-0), buccaneer(4-2-0)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fsunken_columns%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-4), sniper(4-0-2), tack(4-0-2), buccaneer(4-2-0)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fsunken_columns%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(0-2-4), heli(4-0-3), sniper(4-0-2), village(2-2-0), buccaneer(4-2-0)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fsunken_columns%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-4), sniper(4-0-2), tack(4-0-2), buccaneer(4-2-0)">with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fsunken_columns%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: wizard(0-2-4), heli(4-0-3), sniper(4-0-2), village(2-2-0), buccaneer(4-2-0)">supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>X factor</th>
		<td><a href="playthroughs%2Fx_factor%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), tack(4-0-2), heli(4-0-4)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fx_factor%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), tack(4-0-2), heli(4-0-4)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fx_factor%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), tack(4-0-2), heli(4-0-4)">with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Mesa</th>
		<td><a href="playthroughs%2Fmesa%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), heli(4-0-4), tack(4-0-2)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fmesa%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), heli(4-0-4), tack(4-0-2)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fmesa%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), sniper(4-0-2), heli(4-0-4), tack(4-0-2)">with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Geared</th>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fgeared%23deflation%232560x1440%23noLL.btd6"title="required monkeys: heli(3-2-3), ace(2-2-3)">with MK, Psi, military monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td>changing monkey positions (1)</td>
	</tr>
	<tr>
	<th>Spillway</th>
		<td><a href="playthroughs%2Fspillway%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: ninja(2-0-4), buccaneer(4-4-0), heli(4-0-3)"><i>with MK, Etienne, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fspillway%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-1), buccaneer(5-2-0), heli(4-0-3)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fspillway%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: ninja(2-0-4), buccaneer(4-4-0), heli(4-0-3)"><i>with MK, Etienne, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fspillway%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-1), buccaneer(5-2-0), heli(4-0-3)"><i>supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fspillway%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: ninja(2-0-4), buccaneer(4-4-0), heli(4-0-3)">with MK, Etienne, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fspillway%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: ninja(2-0-1), buccaneer(5-2-0), heli(4-0-3)">supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Cargo</th>
		<td><a href="playthroughs%2Fcargo%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-4), tack(4-2-0), buccaneer(4-2-0), druid(3-0-2), ninja(2-0-4)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcargo%23hard%232560x1440%23noMK%23noLLwMK%23chimpsPotential.btd6"title="required monkeys: dart(0-0-0), sniper(2-0-5), spike(0-3-5), village(3-0-2), wizard(4-2-5), alchemist(4-3-1), glue(0-1-4)"><i>supported, Obyn_greenfoot, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcargo%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-4), tack(4-2-0), buccaneer(4-2-0), druid(3-0-2), ninja(2-0-4)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcargo%23hard%232560x1440%23noMK%23noLLwMK%23chimpsPotential.btd6"title="required monkeys: dart(0-0-0), sniper(2-0-5), spike(0-3-5), village(3-0-2), wizard(4-2-5), alchemist(4-3-1), glue(0-1-4)"><i>supported, Obyn_greenfoot, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcargo%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), heli(4-0-4), tack(4-2-0), buccaneer(4-2-0), druid(3-0-2), ninja(2-0-4)">with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fcargo%23hard%232560x1440%23noMK%23noLLwMK%23chimpsPotential.btd6"title="required monkeys: dart(0-0-0), sniper(2-0-5), spike(0-3-5), village(3-0-2), wizard(4-2-5), alchemist(4-3-1), glue(0-1-4)">supported, Obyn_greenfoot, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Pat's pond</th>
		<td><a href="playthroughs%2Fpats_pond%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: sub(0-2-2), wizard(0-2-5), village(2-0-2), spike(3-2-4), alchemist(4-0-0), heli(4-0-2)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fpats_pond%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: sub(0-2-2), wizard(0-2-5), village(2-0-2), spike(3-2-4), alchemist(4-0-0), heli(4-0-2)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fpats_pond%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: sub(0-2-2), wizard(0-2-5), village(2-0-2), spike(3-2-4), alchemist(4-0-0), heli(4-0-2)">supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Peninsula</th>
		<td><a href="playthroughs%2Fpeninsula%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: buccaneer(4-4-0), sniper(4-0-2), heli(4-0-4), tack(4-0-2)"><i>with MK, Etienne, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fpeninsula%23hard%232560x1440%23noMK%23noLL%23chimpsPotential.btd6"title="required monkeys: dart(0-0-2), sniper(4-5-2), spike(0-2-5), alchemist(4-3-1), village(4-0-2), boomerang(2-0-4), glue(0-2-3)"><i>supported, Psi, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fpeninsula%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: buccaneer(4-4-0), sniper(4-0-2), heli(4-0-4), tack(4-0-2)"><i>with MK, Etienne, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fpeninsula%23hard%232560x1440%23noMK%23noLL%23chimpsPotential.btd6"title="required monkeys: dart(0-0-2), sniper(4-5-2), spike(0-2-5), alchemist(4-3-1), village(4-0-2), boomerang(2-0-4), glue(0-2-3)"><i>supported, Psi, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fpeninsula%23hard%232560x1440%23noLLwMK.btd6"title="required monkeys: buccaneer(4-4-0), sniper(4-0-2), heli(4-0-4), tack(4-0-2)">with MK, Etienne, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fpeninsula%23hard%232560x1440%23noMK%23noLL%23chimpsPotential.btd6"title="required monkeys: dart(0-0-2), sniper(4-5-2), spike(0-2-5), alchemist(4-3-1), village(4-0-2), boomerang(2-0-4), glue(0-2-3)">supported, Psi, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>High finance</th>
		<td><a href="playthroughs%2Fhigh_finance%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: buccaneer(4-4-0), village(2-2-0), sniper(4-0-2), heli(4-0-2), tack(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fhigh_finance%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: buccaneer(4-4-0), village(2-2-0), sniper(4-0-2), heli(4-0-2), tack(4-0-2)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fhigh_finance%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: buccaneer(4-4-0), village(2-2-0), sniper(4-0-2), heli(4-0-2), tack(4-0-2)">supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Another brick</th>
		<td><a href="playthroughs%2Fanother_brick%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), buccaneer(5-2-0), heli(4-0-3)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fanother_brick%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-2-0), village(2-2-0), heli(4-0-3)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fanother_brick%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), buccaneer(5-2-0), heli(4-0-3)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fanother_brick%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-2-0), village(2-2-0), heli(4-0-3)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fanother_brick%23hard%232560x1440%23noLL.btd6"title="required monkeys: engineer(4-2-0), buccaneer(5-2-0), heli(4-0-3)">with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fanother_brick%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: buccaneer(5-2-0), village(2-2-0), heli(4-0-3)">supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Off the coast</th>
		<td><a href="playthroughs%2Foff_the_coast%23hard%232560x1440%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), heli(4-0-3)"><i>with MK, Etienne, military monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Foff_the_coast%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: buccaneer(5-2-0), village(3-2-0), tack(3-0-2), heli(4-0-3)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Foff_the_coast%23hard%232560x1440%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), heli(4-0-3)"><i>with MK, Etienne, military monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Foff_the_coast%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: buccaneer(5-2-0), village(3-2-0), tack(3-0-2), heli(4-0-3)"><i>supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Foff_the_coast%23hard%232560x1440%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), heli(4-0-3)"><i>with MK, Etienne, military monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Foff_the_coast%23hard%232560x1440%23noLL.btd6"title="required monkeys: buccaneer(5-4-0), heli(4-0-3)">with MK, Etienne, military monkeys only, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Foff_the_coast%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: buccaneer(5-2-0), village(3-2-0), tack(3-0-2), heli(4-0-3)">supported, Sauda, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Cornfield</th>
		<td><a href="playthroughs%2Fcornfield%23hard%232560x1440%23noLL.btd6"title="required monkeys: tack(4-0-2), ninja(2-0-4), heli(4-0-3), glue(5-2-0)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcornfield%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(2-2-0)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcornfield%23hard%232560x1440%23noLL.btd6"title="required monkeys: tack(4-0-2), ninja(2-0-4), heli(4-0-3), glue(5-2-0)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fcornfield%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(2-2-0)"><i>supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fcornfield%23hard%232560x1440%23noLL.btd6"title="required monkeys: tack(4-0-2), ninja(2-0-4), heli(4-0-3), glue(5-2-0)">with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Fcornfield%23hard%232560x1440%23noMK%23noLL.btd6"title="required monkeys: tack(4-0-2), heli(4-0-3), village(2-2-0)">supported, Sauda, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Underground</th>
		<td><a href="playthroughs%2Funderground%23hard%232560x1440%23noLL.btd6"title="required monkeys: tack(4-0-4), ninja(2-0-4), heli(4-0-3)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Funderground%23hard%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), sniper(4-0-2), heli(4-0-4), ninja(3-0-1), village(2-2-0)"><i>supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Funderground%23hard%232560x1440%23noLL.btd6"title="required monkeys: tack(4-0-4), ninja(2-0-4), heli(4-0-3)"><i>with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Funderground%23hard%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), sniper(4-0-2), heli(4-0-4), ninja(3-0-1), village(2-2-0)"><i>supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Funderground%23hard%232560x1440%23noLL.btd6"title="required monkeys: tack(4-0-4), ninja(2-0-4), heli(4-0-3)">with MK, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a><br><br><a href="playthroughs%2Funderground%23hard%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), sniper(4-0-2), heli(4-0-4), ninja(3-0-1), village(2-2-0)">supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr style="border-top: 2px solid white">
	<th>Glacial trail</th>
	<td rowspan=12>expert</th>
		<td><a href="playthroughs%2Fglacial_trail%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(5-2-0), engineer(5-2-0), druid(1-3-0), mortar(0-2-3), spike(2-0-5), alchemist(4-2-0), glue(0-2-4), ice(5-1-0), ace(4-0-0)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fglacial_trail%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-0), druid(0-0-0), wizard(0-3-2), spike(4-2-5), alchemist(4-3-1), farm(0-2-3), ninja(0-0-4), ace(5-2-0), mortar(0-2-4)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fglacial_trail%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(5-2-0), engineer(5-2-0), druid(1-3-0), mortar(0-2-3), spike(2-0-5), alchemist(4-2-0), glue(0-2-4), ice(5-1-0), ace(4-0-0)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fglacial_trail%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-0), druid(0-0-0), wizard(0-3-2), spike(4-2-5), alchemist(4-3-1), farm(0-2-3), ninja(0-0-4), ace(5-2-0), mortar(0-2-4)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fglacial_trail%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(5-2-0), engineer(5-2-0), druid(1-3-0), mortar(0-2-3), spike(2-0-5), alchemist(4-2-0), glue(0-2-4), ice(5-1-0), ace(4-0-0)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a><br><br><a href="playthroughs%2Fglacial_trail%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-0), druid(0-0-0), wizard(0-3-2), spike(4-2-5), alchemist(4-3-1), farm(0-2-3), ninja(0-0-4), ace(5-2-0), mortar(0-2-4)"><i>supported, Sauda, native: 1920x1080, tested for: 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fglacial_trail%23alternate_bloons_rounds%231920x1080%23noMK%23noLLwMK.btd6"title="required monkeys: druid(1-3-0), sniper(1-1-2), spike(4-2-0), farm(0-2-3), alchemist(4-2-0), dart(5-0-2), wizard(4-0-2)">supported, Sauda, (*), native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fglacial_trail%23impoppable%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-0), druid(0-0-0), wizard(0-3-2), spike(4-2-5), alchemist(4-3-1), farm(0-2-3), ninja(0-0-4), ace(5-2-0), mortar(0-2-4)">supported, Sauda, native: 1920x1080, tested for: 1920x1080</a></td>
		<td><a href="playthroughs%2Fglacial_trail%23chimps%231920x1080%23noMK%23noLL.btd6"title="required monkeys: dart(5-2-0), engineer(5-2-0), druid(1-3-0), mortar(0-2-3), spike(2-0-5), alchemist(4-2-0), glue(0-2-4), ice(5-1-0), ace(4-0-0)">supported, Sauda, native: 1920x1080, tested for: 1920x1080</a></td>
		<td></td>
	</tr>
	<tr>
	<th>Dark dungeons</th>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Sanctuary</th>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fsanctuary%23deflation%232560x1440%23noMK%23noLL.btd6"title="required monkeys: village(2-0-2), super(2-0-3)">supported, Captain_churchill, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td>changing monkey positions (1)</td>
	</tr>
	<tr>
	<th>Ravine</th>
		<td><a href="playthroughs%2Fravine%23hard%232560x1440.btd6"title="required monkeys: dart(0-2-4), sniper(4-0-2), wizard(2-0-4), spike(4-2-0), alchemist(4-2-0), ice(0-3-2), heli(2-0-3)"><i>with MK, Benjamin, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td><a href="playthroughs%2Fravine%23deflation%232560x1440%23noMK%23noLL.btd6"title="required monkeys: village(2-2-2), ace(2-0-3), alchemist(4-0-1)">supported, Captain_churchill, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Fravine%23hard%232560x1440.btd6"title="required monkeys: dart(0-2-4), sniper(4-0-2), wizard(2-0-4), spike(4-2-0), alchemist(4-2-0), ice(0-3-2), heli(2-0-3)"><i>with MK, Benjamin, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fravine%23hard%232560x1440.btd6"title="required monkeys: dart(0-2-4), sniper(4-0-2), wizard(2-0-4), spike(4-2-0), alchemist(4-2-0), ice(0-3-2), heli(2-0-3)">with MK, Benjamin, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Flooded valley</th>
		<td><a href="playthroughs%2Fflooded_valley%23hard%232560x1440%23noMK.btd6"title="required monkeys: sub(2-0-4), buccaneer(0-2-0), spike(4-0-2), village(2-0-2), alchemist(4-0-1), sniper(3-3-2), wizard(4-2-0)"><i>supported, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fflooded_valley%23hard%232560x1440%23noMK.btd6"title="required monkeys: sub(2-0-4), buccaneer(0-2-0), spike(4-0-2), village(2-0-2), alchemist(4-0-1), sniper(3-3-2), wizard(4-2-0)"><i>supported, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fflooded_valley%23hard%232560x1440%23noMK.btd6"title="required monkeys: sub(2-0-4), buccaneer(0-2-0), spike(4-0-2), village(2-0-2), alchemist(4-0-1), sniper(3-3-2), wizard(4-2-0)">supported, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Infernal</th>
		<td><a href="playthroughs%2Finfernal%23hard%232560x1440%23noMK%23noLLwMK%23chimpsPotential.btd6"title="required monkeys: dart(0-2-5), sub(2-0-3), sniper(1-0-1), village(2-2-0), heli(5-0-2), alchemist(4-0-1), wizard(0-2-5), spike(3-2-0)"><i>supported, Quincy, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td><a href="playthroughs%2Finfernal%23deflation%232560x1440%23noMK%23noLL.btd6"title="required monkeys: boomerang(2-0-2), sniper(4-2-4)">supported, Etienne, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td><a href="playthroughs%2Finfernal%23hard%232560x1440%23noMK%23noLLwMK%23chimpsPotential.btd6"title="required monkeys: dart(0-2-5), sub(2-0-3), sniper(1-0-1), village(2-2-0), heli(5-0-2), alchemist(4-0-1), wizard(0-2-5), spike(3-2-0)"><i>supported, Quincy, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Finfernal%23hard%232560x1440%23noMK%23noLLwMK%23chimpsPotential.btd6"title="required monkeys: dart(0-2-5), sub(2-0-3), sniper(1-0-1), village(2-2-0), heli(5-0-2), alchemist(4-0-1), wizard(0-2-5), spike(3-2-0)">supported, Quincy, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Bloody puddles</th>
		<td><a href="playthroughs%2Fbloody_puddles%23hard%232560x1440%23noMK%23RNG.btd6"title="required monkeys: sub(2-0-3), dart(0-0-2), sniper(4-5-5), druid(0-3-0), village(2-0-2), alchemist(4-2-1), glue(1-1-0)"><i>supported, Quincy, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fbloody_puddles%23hard%232560x1440%23noMK%23RNG.btd6"title="required monkeys: sub(2-0-3), dart(0-0-2), sniper(4-5-5), druid(0-3-0), village(2-0-2), alchemist(4-2-1), glue(1-1-0)"><i>supported, Quincy, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fbloody_puddles%23hard%232560x1440%23noMK%23RNG.btd6"title="required monkeys: sub(2-0-3), dart(0-0-2), sniper(4-5-5), druid(0-3-0), village(2-0-2), alchemist(4-2-1), glue(1-1-0)">supported, Quincy, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Workshop</th>
		<td><a href="playthroughs%2Fworkshop%23hard%232560x1440.btd6"title="required monkeys: spike(4-2-0), alchemist(4-2-0), heli(4-0-3), tack(4-0-2)"><i>with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fworkshop%23hard%232560x1440.btd6"title="required monkeys: spike(4-2-0), alchemist(4-2-0), heli(4-0-3), tack(4-0-2)"><i>with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fworkshop%23hard%232560x1440.btd6"title="required monkeys: spike(4-2-0), alchemist(4-2-0), heli(4-0-3), tack(4-0-2)">with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Quad</th>
		<td><a href="playthroughs%2Fquad%23hard%232560x1440%23noMK.btd6"title="required monkeys: dart(0-0-0), sub(2-0-2), wizard(0-3-2), sniper(1-0-0), spike(3-2-0), ice(4-1-3), village(4-0-2), alchemist(3-0-0), bomb(2-0-3), tack(2-0-4), glue(0-1-3)"><i>supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fquad%23medium%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), ninja(4-0-1), buccaneer(4-3-2), village(0-2-0), heli(2-0-3), sniper(3-0-2)"><i>supported, -, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fquad%23hard%232560x1440%23noMK.btd6"title="required monkeys: dart(0-0-0), sub(2-0-2), wizard(0-3-2), sniper(1-0-0), spike(3-2-0), ice(4-1-3), village(4-0-2), alchemist(3-0-0), bomb(2-0-3), tack(2-0-4), glue(0-1-3)"><i>supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fquad%23medium%232560x1440%23noMK.btd6"title="required monkeys: tack(4-0-2), ninja(4-0-1), buccaneer(4-3-2), village(0-2-0), heli(2-0-3), sniper(3-0-2)">supported, -, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fquad%23hard%232560x1440%23noMK.btd6"title="required monkeys: dart(0-0-0), sub(2-0-2), wizard(0-3-2), sniper(1-0-0), spike(3-2-0), ice(4-1-3), village(4-0-2), alchemist(3-0-0), bomb(2-0-3), tack(2-0-4), glue(0-1-3)">supported, Sauda, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>Dark castle</th>
		<td><a href="playthroughs%2Fdark_castle%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-2), sub(2-0-3), alchemist(4-2-0), super(3-0-2), village(2-0-2), spike(3-2-5), sniper(4-0-2), boomerang(0-2-4), glue(0-1-3), mortar(0-0-4)"><i>supported, Obyn_greenfoot, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fdark_castle%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: sub(0-0-0), dart(0-0-0), spike(0-2-3), druid(0-1-4), alchemist(4-2-0), village(2-2-0)"><i>supported, Obyn_greenfoot, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fdark_castle%23primary_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), boomerang(3-0-2), dart(0-2-4)"><i>supported, Sauda, primary monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td><a href="playthroughs%2Fdark_castle%23primary_only%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: tack(4-0-2), boomerang(3-0-2), dart(0-2-4)">supported, Sauda, primary monkeys only, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td><a href="playthroughs%2Fdark_castle%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-2), sub(2-0-3), alchemist(4-2-0), super(3-0-2), village(2-0-2), spike(3-2-5), sniper(4-0-2), boomerang(0-2-4), glue(0-1-3), mortar(0-0-4)"><i>supported, Obyn_greenfoot, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fdark_castle%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: sub(0-0-0), dart(0-0-0), spike(0-2-3), druid(0-1-4), alchemist(4-2-0), village(2-2-0)"><i>supported, Obyn_greenfoot, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fdark_castle%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-2), sub(2-0-3), alchemist(4-2-0), super(3-0-2), village(2-0-2), spike(3-2-5), sniper(4-0-2), boomerang(0-2-4), glue(0-1-3), mortar(0-0-4)"><i>supported, Obyn_greenfoot, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a><br><br><a href="playthroughs%2Fdark_castle%23hard%232560x1440%23noMK%23noLLwMK.btd6"title="required monkeys: sub(0-0-0), dart(0-0-0), spike(0-2-3), druid(0-1-4), alchemist(4-2-0), village(2-2-0)">supported, Obyn_greenfoot, (*), native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fdark_castle%23alternate_bloons_rounds%232560x1440.btd6"title="required monkeys: spike(0-2-4), druid(0-2-4), sniper(1-2-0), ninja(0-0-1), village(2-2-0), alchemist(4-2-0)">with MK, Obyn_greenfoot, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td><a href="playthroughs%2Fdark_castle%23chimps%232560x1440%23noMK%23noLL.btd6"title="required monkeys: dart(0-0-2), sub(2-0-3), alchemist(4-2-0), super(3-0-2), village(2-0-2), spike(3-2-5), sniper(4-0-2), boomerang(0-2-4), glue(0-1-3), mortar(0-0-4)">supported, Obyn_greenfoot, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
	</tr>
	<tr>
	<th>Muddy puddles</th>
		<td><a href="playthroughs%2Fmuddy_puddles%23hard%232560x1440.btd6"title="required monkeys: buccaneer(4-2-0), sub(2-0-4), village(0-2-0), heli(4-0-2), tack(4-0-2), wizard(4-2-0), spike(3-2-0)"><i>with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fmuddy_puddles%23hard%232560x1440.btd6"title="required monkeys: buccaneer(4-2-0), sub(2-0-4), village(0-2-0), heli(4-0-2), tack(4-0-2), wizard(4-2-0), spike(3-2-0)"><i>with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fmuddy_puddles%23hard%232560x1440.btd6"title="required monkeys: buccaneer(4-2-0), sub(2-0-4), village(0-2-0), heli(4-0-2), tack(4-0-2), wizard(4-2-0), spike(3-2-0)">with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr>
	<th>#Ouch</th>
		<td><a href="playthroughs%2Fouch%23hard%232560x1440.btd6"title="required monkeys: engineer(4-2-0), village(2-2-0), heli(4-0-3), wizard(0-2-4), sniper(4-0-2)"><i>with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fouch%23hard%232560x1440.btd6"title="required monkeys: engineer(4-2-0), village(2-2-0), heli(4-0-3), wizard(0-2-4), sniper(4-0-2)"><i>with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</i></a></td>
		<td></td>
		<td></td>
		<td></td>
		<td><a href="playthroughs%2Fouch%23hard%232560x1440.btd6"title="required monkeys: engineer(4-2-0), village(2-2-0), heli(4-0-3), wizard(0-2-4), sniper(4-0-2)">with MK, Psi, *, native: 2560x1440, tested for: 2560x1440, 1920x1080</a></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
</table>
</div>

(1): Maps with changing monkey positions are currently not recordable/replayable in any mode other than deflation
<br>
(2): Maps with changing position and monkey accessibility are currently not recordable/replayable in any mode other than deflation

# Recording playthroughs

Playthroughs can be recorded using `record_playthrough.py`.
<br>
Usage: `py record_playthrough.py [-e]`

`-e` flag is used when you want to extend upon an existing playthrough file.

After starting the script you must specify which map, gamemode and hero you are using.
If you are not using a hero just specify any like `quincy`.

After that you can switch to BTD6 and do the playthrough.

Actions are only recorded when BTD6 is your active window and your cursor is inside BTD6.

### Placing a monkey

To place a monkey first select it in the GUI and hover to the position you want to place it at (to check whether it can be placed there). After that press escape to unselect the monkey and then press the keybind corresponding to the monkey you want to place and place it. When pressing the keybind the position of your cursor will be logged as the monkeys position. 

If your keybinds differ from the default keybinds you will need to change them in `keybinds.json` (see [Keybinds](#keybinds)).

### Removing an obstacle

To log the removal of an obstacle you must press the right shift button while at a position the obstacle is clickable from.

After finishing the recording (by pressing ctrl + c) you are prompted to enter the cost of each obstacle removal in the order they were removed.

### Selecting a monkey

The following operations all require a monkey to be selected. This can be done by pressing the left ctrl key while in proximity of the monkey to select. This will select the monkey closest to your cursors position. The name of the selected monkey will be printed in the console.

### Upgrading a monkey

To upgrade a monkey you can, after selecting the monkey, simply press the key corresponding to the path you want to upgrade.

### Retargeting a monkey

To retarget a monkey you can, after selecting the monkey, simply press the key corresponding to the right retarget arrow (defaults to tab) as many times as required.
<br>
For dartling and mortar monkeys retargeting requires a position. A retarget with a position can be logged by pressing space while pressing tab. This will use your cursors current position.

### Activating monkey special

To activate/deactivate a monkeys monkey special (e. g. prioritize camo) you can, after selecting the monkey, simply press the corresponding key (defaults to page down).

### Selling monkeys

To sell a monkey you can, after selecting the monkey, simply press the corresponding key (defaults to backspace). When replaying a recording a sell occurs once your current money + the money gained from this and all adjacent sells surpasses the money required for the next non selling action (which could be 0 for retargeting/monkey special). Ideally you want to avoid selling when using monkey knowledge as the sell could result in less money than expected (due to reduced cost, which isn't factored in)(i. e. your towers are sold before you can actually afford the next tower or upgrade).

### Awaiting a round

To await a round you must press the left shift button.

Directly after the script will prompt you to enter the round you want to await. Entering something invalid aborts the creation of the await round entry. The specified round must be greater than 0 as well as any previously awaited round!

### Monkey naming

Monkeys in the playthrough file are named `<type><number of monkeys of this type placed>` e. g. `sniper0` for the first sniper monkey placed, `sniper1` for the next one etc.

Types are:
- `dart`
- `boomerang`
- `bomb`
- `tack`
- `ice`
- `glue`
- `sniper`
- `sub`
- `buccaneer`
- `ace`
- `heli`
- `mortar`
- `dartling`
- `wizard`
- `super`
- `ninja`
- `alchemist`
- `druid`
- `farm`
- `engineer`
- `spike`
- `village`
- `beasthandler`
- `mermonkey`

### Stop recording

To stop recording press `ctrl` + `c` while in the console `record_playthrough.py` is running in.

### Editing a playthrough afterwards

The playthrough file can be edited after recording (e. g. to correct/remove accidental keypresses). The corresponding file is saved under `own_playthroughs/<map>#<gamemode>#<resolution>.btd6` (e. g. `own_playthroughs/cornfield#hard#2560x1440.btd6`).

Valid entries in a file are:
- placing a monkey (e. g. `place ninja ninja0 at 1212, 641` or for heros `place etienne hero0 at 1212, 641`)
- upgrading a monkey (e. g. `upgrade ninja0 path 0`)
- retargeting a monkey (clicking the right retarget arrow once) (e. g. `retarget ninja0`)
- retargeting a monkey to a position (e. g. `retarget dartling0 to 123, 321`)
- activate/deactivate monkey special (e. g. prioritize camo) (e. g. `special ninja0`)
- selling a monkey (e. g. `sell ninja0`)
- removing an obstacle (e. g. `remove obstacle at 123, 321 for 500`)
- awaiting a round (e. g. `round 27`)
- specifing the gamespeed (`speed fast` or `speed slow`). The speed defaults to `fast`.

Additionally you can specify a discount for an upgrade/placement by appending `with <n>% discount` where n an integer between 0 and 100 (including 100 e. g. with the `primary mentoring` upgrade for villages) representing the discount in percent. This may be useful when upgrading a village to `monkey business` or `monkey commerce` and the resulting discount is critical for the playthrough to work.
Note that discounts stack by simply being added (e. g. 2 Villages with `monkey commerce` in radius result in a discount of 10%+5%+5% = 20%). E. g. a valid entry would be `upgrade ninja0 path 2 with 20% discount`.

There are also several flags that can be used in the filename:
- `#noMK` - to specify no monkey knowledge was used
- `#noLL` - no lives lost
- `#noLLwMK` - no lives lost with arbitrary monkey knowledge (only `#noLL` or `#noLLwMK`)
  
a resulting filename could be: `high_finance#hard#2560x1440#noMK#noLLwMK.btd6`
for a playthrough of high finance on hard with no monkey knowledge required and no lives lost when using arbitrary monkey knowledge (probably mana lives or free roadspikes)

## Contributing playthroughs

Playthroughs for contribution should be recorded with monkey knowledge disabled. Please specify whether this condition was met when contributing playthroughs.

Additionally playthroughs should ideally use popular screen resolutions (like 1920x1080, 2560x1440 or 3840x2160) as rescaled playthroughs may not work (due to impossible placements etc.).

If you want to contribute playthroughs you can do it by either forking the repository and creating a pull request with the playthrough files added or you can create an issue with the playthrough file content as a code block.

## Beast Handler

Due to a lack of hotkeys features like merging beast handlers or targeting beasts are currently unsupported. As a result tier 5 beast handlers can't be used, as they require merging.

# Additional scripts

The repository contains some additional scripts:

`convert_playthrough.py`<br>
Usage: `py convert_playthrough.py <filename> <resolution(e. g. 1920x1080)>`<br>
Converts playthrough `filename` to the provided resolution and saves it under `own_playthroughs/<filename>` but with replaced resolution.
Can be used to tweak positions in a converted playthrough that doesn't work out of the box.

`make_screenshot.py`<br>
Usage: `py make_screenshot.py`<br>
Takes a screenshot of your primary screen and saves it in the `screenshots` folder. For taking screenshots required to support new resolutions.

`convert_image_to_mask.py`<br>
Usage: `py convert_image_to_mask.py <filename>`<br>
Takes a png image and converts all red (#FF0000) pixels to white, all other to black and saves it under the same filename with `_masked` appended. Used internally for cv2.matchTemplate mask.

`log_keypresses.py`<br>
Usage: `py log_keypresses.py`<br>
Prints the data of key events including keyname and scancode. Used for changing `keybinds.json`. Stop by pressing `ctrl` + `c`.

`generate_supported_maps_table.py`<br>
Usage `py generate_supported_maps_table.py`<br>
Updates the table of supported playthroughs in `README.md` by scaning the `playthroughs` folder.

`ocr_image.py`<br>
Usage `py ocr_image.py <filename>`<br>
Outputs the detected balance and saves the relevant area of the image as seen by the programm under the same filename with `_area` appended.

# Supported resolutions

Currently only screen resolutions of `1920x1080` and `2560x1440` are supported. Supporting a resolution requires the images in the folder `images/<resolution>` (as well as tested rescaled or native playthroughs).

# Supporting new collection events

Supporting a new collection event only requires adding a `.png` image of the symbol on a map to the `images/<resolution>/collection_events` folder. Similar to `images/<resolution>/collection_events/totem.png`. The collection event name will be the filename without `.png`.

# Supporting new versions of Bloons TD6

Most changes that get introduced in updates can be incorporated by adapting the corresponding config files:

Update `version.txt` to contain the new version.

**Please be aware that balance changes in major as well as minor updates to BTD6 could cause the provided playthroughs to no longer work.**<br>
Regardless newly recorded playthroughs will work.

## Adding new maps

New Maps can be added by running `insert_new_map.py`.<br>
Usage: `py insert_new_map.py "<name of the new map>" <before|after> "<name of adjacent map>"`<br>
e. g. `py insert_new_map.py "Midnight mansion" before "Sunken columns"`<br>
This will update `maps.json` by inserting the new map and shifting all following maps of the same category by one position.

## Incorporating balance changes in regards to tower/upgrade cost

The prices can be automatically updated by running the [`costs`](#costs---determine-cost-of-each-monkey-upgrade-and-hero) mode.

## Adding new towers

Adding a new tower requires adding it to `towers.json` -> `monkeys`.
- `base` refers to the towers base cost
- `class` describes where the tower can be placed (`land`, `water` or `any` (meaning both, like pat futsy))
- `upgrades` refer to the cost of each upgrade (cost on medium difficulty with monkey knowledge disabled)
- (optional) `upgrade_confirmation` describes whether the upgrade has a confirmation dialog (currently only used for super monkeys)(no dialog if omitted)

Additionally you need to provide the corresponding hotkey in `keybinds.json`.

The addition is only required if you plan to use said tower.

## Adding new heros

Adding a new tower requires adding it to `towers.json` -> `heros`.
- `base` refers to the towers base cost
- `class` describes where the tower can be placed (`land`, `water` or `any` (meaning both, like pat futsy))

Additionally you need to provide the coordinates in the hero selection menu in `image_areas.json` for a resolution of 2560x1440.<br>
If the hero shifts the positions of other heros the positions of affected heros will need to be changed as well.<br>
If the hero selection menu gets reorganized for the 16th+ hero all coordinates will need to be updated.

## Major GUI changes

If the GUI of BTD6 changes majorly you might need to recreate the screenshots in `images/<resolution>` for your resolution or even redefine the characteristic areas in `image_areas.json` for said screenshots. If you define a new resolution in `image_areas.json` all attributes present in `2560x1440` must be defined!

# Known issues

- abilities can't be used as they require timing
- the price calculation currently doesn't fully factor in monkey knowledge. (currently only `hero favors` for reduced hero cost)
