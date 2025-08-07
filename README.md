# TriMEph
## Basic description
TriMEph is an object-oriented software designed to compute and visualize temperature trends of the Mössbauer factor in materials. It uses mean square displacement of atoms evaluated from phonon modes as input - the input files are output files of the PHONOPY software, e.g. the phonopy.yaml file. The Mössbauer effect plays a crucial role in our atomic-scale probing and understanding of materials. It is based on interactions of gamma rays with atomic nuclei and the Mössbauer factor is a key parameter in describing this interaction. The authors (Filip Pomajbo, Nikolas Masničák and Martin Friák) gratefully acknowledge financial support from the Czech Science Foundation, Project No. 22-05801S.

Repository layout:
- .gitignore                   – ignore build artifacts, cache, envs
- build.bat                    – Windows build script (PyInstaller)
- examples/                    – sample input data files
- resources/                   – static assets bundled with the app
  - backround.jpg                – background image
  - User Manual.pdf           – user manual
  - LICENCE.txt                – MIT license copy
- LICENSE                      – MIT license (root copy)
- README.md                    – this overview + instructions
- requirements.txt             – Python dependencies
- TriMEph.py                   – main Python source file

How to build the executable:
1. Install dependencies:
   pip install -r requirements.txt
2. From the project root (where TriMEph.py and build.bat live), run:
   build.bat
   – this cleans old builds and calls PyInstaller in one-file mode, embedding icon and resources
3. On success you will find dist\TriMEph.exe

How to create a user-friendly release bundle:
1. Create a folder named TriMEph_vX.Y (e.g. TriMEph_v1.0)
2. Copy into it:
   • dist\TriMEph.exe
   • resources\backround.jpg
   • resources\User Manual.pdf
   • resources\LICENCE.txt
   • the entire examples\ folder
3. Archive that folder as a .zip or .tar.gz and distribute it

Please send any bug reports or support requests to TriMEph.support@ipm.cz

