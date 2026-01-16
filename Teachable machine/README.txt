Place your Teachable Machine image model export here.

Expected structure inside this folder (exact filenames from TM export):
- model.json
- metadata.json
- weights files (binary files created by export)

Once placed, the camera page (`Camera.html`) will automatically try to load the model from `./Teachable machine/`.

If the folder name contains a space (as here), the web server serves it fine for localhost. If you run into any path issues, rename to `Teachable_machine` and update `Camera.html` accordingly.