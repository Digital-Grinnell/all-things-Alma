Julia Bauder
 
alma-d
Jul 8th at 4:02 PM
Seen today on the Alma-D mailing list: "You can use a combination of Analytics and scripting using the Amazon S3 APIs to bulk download content from your Alma digital storage.
"Analytics will have the file path where the objects are stored; "File Details"."File Internal Path"
"You’d then need to use that path to download the file(s) from your Alma’s Amazon S3 storage.
 *  https://urldefense.proofpoint.com/v2/url?u=https-3A__developers.exlibrisgroup.com_alma_integrations_digital_almadigital_&d=DwIGaQ&c=HUrdOLg_tCr0UMeDjWLBOM9lLDRpsndbROGxEKQRFzk&r=635534ScZfXSRDpdzWobNE_dcO1rW4hQ5FtRlzG9QFY&m=F_CyvZXVhqMjG5PPyielLwL_CHVvf1dPuLBvTzwWZJ4hegDljdxCtzeRt7jnliPF&s=-6skRLr8tmYku8syXfl8cwJSX7-Krq5uP3auybF7z90&e=
"We’ve done this exact thing using PowerShell scripts (using Copy-S3Object) previously, and it works without fault.
 *  https://docs.aws.amazon.com/powershell/v5/userguide/powershell_s3_code_examples.html
"Reach out if you’d like specific examples and/or guidance.
Cheers,
Ben
Ben Dalwood
Manager, Library Applications | University Library
The University of Adelaide"