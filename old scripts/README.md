# woc3.0-ecommerce-price-tracker-Shantanu-Tyagi

1. Checks for valid URL and then checks if service is available for that website. If yes, continues normal execution. Else, logs the exception.<br>
2. Checks if the product is available on that website. If unvailable continues normal execution. Else logs the exception and continues normal execution.
3. Amazon: Identifies the product type, i.e. normal or deal of the day product. Accordingly scrapes the name, price and downloads the image. These are displayed in the output.<br>
4. Flipkart: Scrapes name and price and first identifies the product type and then scrapes the image accordingly all of which are then displayed in output.<br>
5. Snapdeal: Scrapes the name, price and image and displays it as the output.<br>
6. If scraping is successful with price within specified budget then email is sent with product details, link and image attachment to the user. Execution stops.<br>
7. If email conditions are not met, normal execution continues.<br>
8. Last modified time is logged.<br>
9. Normal ecexcution: Script is run on regular intervals untill email is sent or some exception occurs.<br>
10. If system is shut down, then last modified data is used to decide if execution should start immediately becausse system was down for a time greater than script ecexution interval or after some time because system was shut for a time less than script execution inverval.<br>
