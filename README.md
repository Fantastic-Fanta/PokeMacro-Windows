# Setup Guide

**1. Download the ZIP file from the release called "Main"**
Link: https://github.com/Fantastic-Fanta/PokeMacro-Windows/releases/tag/v1.0.0
This should contain a ZIP file consisting of
- `Configs File` (Configuration file to be edited, Configs.yaml)
- `Configs Tool` (Used to edit co-ordinates of Configs.yaml)
- The main Macro executable named `PokeMacro`
Verify that all 3 things are there

**2. Open the game, run around until you get an egg and ensure the below settings are on**
<img width="791" height="86" alt="Screenshot 2026-02-25 at 4 36 59 AM" src="https://github.com/user-attachments/assets/4a1389b5-b6d8-42ed-8e74-72c79a1f066e" />
<img width="794" height="94" alt="Screenshot 2026-02-25 at 4 37 11 AM" src="https://github.com/user-attachments/assets/29da01fe-36e4-484c-a9d3-1f8d98822e19" />
<img width="680" height="54" alt="Screenshot 2026-02-25 at 4 37 24 AM" src="https://github.com/user-attachments/assets/549ed4dc-b14c-4180-9892-c1eb8bdf2324" />
<img width="681" height="54" alt="Screenshot 2026-02-25 at 4 37 33 AM" src="https://github.com/user-attachments/assets/6668b95c-efaf-4dba-b94b-34c4a12ce1cc" />

**3. Save and rejoin, open the `Configs Tool` in the folder**
Refer to the below images on exactly where to place the points at, please ensure the points are exactly as is because the macro functions off reading color value of pixels


<img width="162" height="66" alt="Screenshot 2026-02-25 at 4 44 04 AM" src="https://github.com/user-attachments/assets/0847015a-6cac-49f3-9cc9-7dd112513101" />
<img width="106" height="63" alt="image" src="https://github.com/user-attachments/assets/bf20b5ef-b10f-4a82-a124-f8ff96a53640" />
<img width="82" height="69" alt="image" src="https://github.com/user-attachments/assets/1e0cdb47-8ae0-4620-9adb-56e581232d16" />
<img width="240" height="53" alt="image" src="https://github.com/user-attachments/assets/0788d306-4a8c-4893-bcb1-9d39a6196072" />
<img width="92.8" height="63.8" alt="image" src="https://github.com/user-attachments/assets/f1b4665a-aacc-4d4c-b6d4-58d843e95358" />

**4. Save the configs, rejoin onto loading screen and open the Macro**
Enter your name, if your name has any of the following, please get a better name:
- Multiple `i`s `l`s or `1`s
- Lowercase `m`
- Crap ton of numbers at the end

<img width="2333" height="1206" alt="image" src="https://github.com/user-attachments/assets/cc470bc5-f05e-4b03-ab37-bd116a96c140" />


**5. Fake a Shiny/Whatever to test if it saves**
Matching criterias:
- IsShiny - stopping at Shiny
- IsReskin - stopping at any Reskin in wishlist (editable in configs)
- IsGradient - stopping at any gradient in wishlist (editable in configs)
- IsAny - stopping at either a Reskin or a Gradient in wishlist
- IsGood - stopping at either a Reskin+Gradient or a Shiny+Gradient (Note: this will NOT stop at Shiny Reskins because there isn't a sprite difference)

**Always only have 1 critera set to `true` at a time and everything else must be `false`, the only exception of this is when you wish to hunt a Reskin+Gradient only where you can tick both `IsReskin` and `IsGradient`, or if you wish to hunt a Shiny+Reskin+Gradient, then you should tick `IsShiny`, `IsGradient` and `IsReskin` all at once.**
