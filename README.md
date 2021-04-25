# Input and output
Raw image with a given name is taken from `img_raw` and is processed and saved to `img`. Then it is signed and saved to `results`.

## How keys are stored
Generated keys are stored in `keys`. A keygroup contains 3 files identified by a similar name. They are
- a `json` file having hash parameters
- an `xml` file of public key
- an `xml` file of private key

# Usage
1. Place a png image named as `IMAGE_NAME.png` in `raw_img` directory. 
2. Assign `IMAGE_NAME` to `image_name` variable in `main.py`.
3. Assign a string value to `key_identifier` variable in `main.py`.
3. Run `python3 main.py`