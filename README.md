## **TTB Label Verifier**

Usage details:

When this link is clicked https://ttblabelverifier-91juk2z5f-yousif-alnomanis-projects.vercel.app/

A form page will be presented to you with the details of the product that you are trying to compare.

The first two fields will be asking for the brand and alcohol type. The inputs are not strictly regulated to where it only accepts names out of certain brands known nationally, but a mere match of the input that the user provides.

For instance, if a user inputs:

**Tommy Hilfigher**

but the only name that is found in the image is **Tommy**, the program assumes that the brand name that the user is searching for within the label is Tommy Hilfigher, and thus does not return a hit. The alcohol type field works the same way.

The ABV% works by exploiting a pattern in alcohol labels, where a % is usually present within the label. The program looks for this number succeeded by the % sign, and sees whether it matches, to the 10ths place, the measurement entered in the form.

Finally, the program detects any numbers int the provided image succeeded by any of the following volume units:

**fl oz, oz (assuming the beverage is the same density as water), liters, milliliters, and centiliters**

Simply input the amount that you want to verify in milliliters, and the program will compare the inputted value to the one detected, and make all (if any) conversions necessary to tell you whether there is a match.

After the form is submitted, a results page will appear to the right of the form. This will include match or hit data for each field. For the numerical values, if a number is detected at all with the correct format (i.e. a % or a valid volume unit preceded by a number), and that number does **not** match the form's, then that number will be shown for the user's convenicence. Additionally, the entirety of the texts detected in the label will be displayed at the bottom right of the page for the user's diagnostic intents.


Note: The label detection is not 100% accurate. OCR technology has come very far, and the best model is being used for this


=============================================================================
## For Developers

How to run a localhost implementation:

Clone the repository's main branch.

Go into server.py, and ensure that the port being used (8080 by default), is free and not occupied by any other applications. If the port is not available, change the code to reflect that on the ```python app.run()``` line.

In the index.tsx file. Ensure that the line which has ```typescript const res = await fetch()```  contains the correct argument that routes it to the server. Ensure that the end of this argument ends in ```api/upload```.

After making any of the previous necessary changes, create a python environment and open two different shell instances. In the first shell instance go into the **server** folder directory and ensure that you have a google vision api key in a json format, and name it vision_key.json so that the server.py file can authenticate API access.

Once that is done, you can run ```bash pip install -r requirements.txt``` and then ```bash python3 server.py``` to get the server running.

The frontend can be run by executing ```bash npm run dev``` in the directory containing index.tsx


