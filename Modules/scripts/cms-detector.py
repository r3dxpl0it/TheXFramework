 # cms-detector.py v0.1
import requests
import argparse


# Mask the user agent so it doesn't show as python and get blocked, set global for request that need to allow for redirects
# Get function to swap the user agent
def get(websiteToScan):
    global user_agent
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    }
    return requests.get(websiteToScan, allow_redirects=False, headers=user_agent)


# Begin scan
def scan():
    # Check to see if the site argument was specified
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", help="Use this option to specify the domain or IP to scan.")
    args = parser.parse_args()
    if args.site is None:
        # Get the input from the user
        print
        print "Please enter the site or IP you would like to scan below."
        print "Examples - www.site.com, https://store.org/magento, 192.168.1.50"
        websiteToScan = raw_input('Site to scan: ')
    else:
        websiteToScan = args.site

    # Check the input for HTTP or HTTPS and then remove it, if nothing is found assume HTTP
    if websiteToScan.startswith('http://'):
        proto = 'http://'
        # websiteToScan = websiteToScan.strip('http://')
        websiteToScan = websiteToScan[7:]
    elif websiteToScan.startswith('https://'):
        proto = 'https://'
        # websiteToScan = websiteToScan.strip('https://')
        websiteToScan = websiteToScan[8:]
    else:
        proto = 'http://'

    # Check the input for an ending / and remove it if found
    if websiteToScan.endswith('/'):
        websiteToScan = websiteToScan.strip('/')

    # Combine the protocol and site
    websiteToScan = proto + websiteToScan

    # Check to see if the site is online
    print
    print "[+] Checking to see if the site is online..."

    try:
        onlineCheck = get(websiteToScan)
    except requests.exceptions.ConnectionError as ex:
        print "[!] " + websiteToScan + " appears to be offline."
    else:
        if onlineCheck.status_code == 200 or onlineCheck.status_code == 301 or onlineCheck.status_code == 302:
            print " |  " + websiteToScan + " appears to be online."
            print
            print "Beginning scan..."
            print
            print "[+] Checking to see if the site is redirecting..."
            redirectCheck = requests.get(websiteToScan, headers=user_agent)
            if len(redirectCheck.history) > 0:
                if '301' in str(redirectCheck.history[0]) or '302' in str(redirectCheck.history[0]):
                    print "[!] The site entered appears to be redirecting, please verify the destination site to ensure accurate results!"
                    print "[!] It appears the site is redirecting to " + redirectCheck.url
            elif 'meta http-equiv="REFRESH"' in redirectCheck.text:
                print "[!] The site entered appears to be redirecting, please verify the destination site to ensure accurate results!"
            else:
                print " | Site does not appear to be redirecting..."
        else:
            print "[!] " + websiteToScan + " appears to be online but returned a " + str(
                onlineCheck.status_code) + " error."
            print
            exit()

        print
        print "[+] Attempting to get the HTTP headers..."
        # Pretty print the headers - courtesy of Jimmy
        for header in onlineCheck.headers:
            try:
                print " | " + header + " : " + onlineCheck.headers[header]
            except Exception as ex:
                print "[!] Error: " + ex.message

        ####################################################
        # WordPress Scans
        ####################################################
        quit()
        print
        #print "[+] Running the WordPress scans..."

        # Use requests.get allowing redirects otherwise will always fail
        wpLoginCheck = requests.get(websiteToScan + '/wp-login.php', headers=user_agent)
        if wpLoginCheck.status_code == 200 and "user_login" in wpLoginCheck.text and "404" not in wpLoginCheck.text:
            print "[!] Detected: WordPress WP-Login page: " + websiteToScan + '/wp-login.php'
            
       # else:
       #     print " |  Not Detected: WordPress WP-Login page: " + websiteToScan + '/wp-login.php'

        # Use requests.get allowing redirects otherwise will always fail
        wpAdminCheck = requests.get(websiteToScan + '/wp-admin', headers=user_agent)
        if wpAdminCheck.status_code == 200 and "user_login" in wpAdminCheck.text and "404" not in wpLoginCheck.text:
            print "[!] Detected: WordPress WP-Admin page: " + websiteToScan + '/wp-admin'
        #else:
        #    print " |  Not Detected: WordPress WP-Admin page: " + websiteToScan + '/wp-admin'

        wpAdminUpgradeCheck = get(websiteToScan + '/wp-admin/upgrade.php')
        if wpAdminUpgradeCheck.status_code == 200 and "404" not in wpAdminUpgradeCheck.text:
            print "[!] Detected: WordPress WP-Admin/upgrade.php page: " + websiteToScan + '/wp-admin/upgrade.php'
        #else:
        #    print " |  Not Detected: WordPress WP-Admin/upgrade.php page: " + websiteToScan + '/wp-admin/upgrade.php'

        wpAdminReadMeCheck = get(websiteToScan + '/readme.html')
        if wpAdminReadMeCheck.status_code == 200 and "404" not in wpAdminReadMeCheck.text:
            print "[!] Detected: WordPress Readme.html: " + websiteToScan + '/readme.html'
       # else:
       #     print " |  Not Detected: WordPress Readme.html: " + websiteToScan + '/readme.html'

        wpLinksCheck = get(websiteToScan)
        if 'wp-' in wpLinksCheck.text:
            print "[!] Detected: WordPress wp- style links detected on index"
        #else:
         #   print " |  Not Detected: WordPress wp- style links detected on index"

        ####################################################
        # Joomla Scans
        ####################################################

        print
       # print "[+] Running the Joomla scans..."

        joomlaAdminCheck = get(websiteToScan + '/administrator/')
        if joomlaAdminCheck.status_code == 200 and "mod-login-username" in joomlaAdminCheck.text and "404" not in joomlaAdminCheck.text:
            print "[!] Detected: Potential Joomla administrator login page: " + websiteToScan + '/administrator/'
       # else:
       #     print " |  Not Detected: Joomla administrator login page: " + websiteToScan + '/administrator/'

        joomlaReadMeCheck = get(websiteToScan + '/readme.txt')
        if joomlaReadMeCheck.status_code == 200 and "joomla" in joomlaReadMeCheck.text and "404" not in joomlaReadMeCheck.text:
            print "[!] Detected: Joomla Readme.txt: " + websiteToScan + '/readme.txt'
       # else:
       #     print " |  Not Detected: Joomla Readme.txt: " + websiteToScan + '/readme.txt'

        joomlaTagCheck = get(websiteToScan)
        if joomlaTagCheck.status_code == 200 and 'name="generator" content="Joomla' in joomlaTagCheck.text and "404" not in joomlaTagCheck.text:
            print "[!] Detected: Generated by Joomla tag on index"
        #else:
        #    print " |  Not Detected: Generated by Joomla tag on index"

        joomlaStringCheck = get(websiteToScan)
        if joomlaStringCheck.status_code == 200 and "joomla" in joomlaStringCheck.text and "404" not in joomlaStringCheck.text:
            print "[!] Detected: Joomla strings on index"
        #else:
        #    print " |  Not Detected: Joomla strings on index"

        joomlaDirCheck = get(websiteToScan + '/media/com_joomlaupdate/')
        if joomlaDirCheck.status_code == 403 and "404" not in joomlaDirCheck.text:
            print "[!] Detected: Joomla media/com_joomlaupdate directories: " + websiteToScan + '/media/com_joomlaupdate/'
        #else:
        #    print " |  Not Detected: Joomla media/com_joomlaupdate directories: " + websiteToScan + '/media/com_joomlaupdate/'

        ####################################################
        # Magento Scans
        ####################################################

        print
       # print "[+] Running the Magento scans..."

        magentoAdminCheck = get(websiteToScan + '/index.php/admin/')
        if magentoAdminCheck.status_code == 200 and 'login' in magentoAdminCheck.text and "404" not in magentoAdminCheck.text:
            print "[!] Detected: Potential Magento administrator login page: " + websiteToScan + '/index.php/admin'
        #else:
        #    print " |  Not Detected: Magento administrator login page: " + websiteToScan + '/index.php/admin'

        magentoRelNotesCheck = get(websiteToScan + '/RELEASE_NOTES.txt')
        if magentoRelNotesCheck.status_code == 200 and 'magento' in magentoRelNotesCheck.text:
            print "[!] Detected: Magento Release_Notes.txt: " + websiteToScan + '/RELEASE_NOTES.txt'
       # else:
        #    print " |  Not Detected: Magento Release_Notes.txt: " + websiteToScan + '/RELEASE_NOTES.txt'

        magentoCookieCheck = get(websiteToScan + '/js/mage/cookies.js')
        if magentoCookieCheck.status_code == 200 and "404" not in magentoCookieCheck.text:
            print "[!] Detected: Magento cookies.js: " + websiteToScan + '/js/mage/cookies.js'
      #  else:
      # #     print " |  Not Detected: Magento cookies.js: " + websiteToScan + '/js/mage/cookies.js'
#
        magStringCheck = get(websiteToScan + '/index.php')
        if magStringCheck.status_code == 200 and '/mage/' in magStringCheck.text or 'magento' in magStringCheck.text:
            print "[!] Detected: Magento strings on index"
       # else:
      #      print " |  Not Detected: Magento strings on index"

            # print magStringCheck.text

        magentoStylesCSSCheck = get(websiteToScan + '/skin/frontend/default/default/css/styles.css')
        if magentoStylesCSSCheck.status_code == 200 and "404" not in magentoStylesCSSCheck.text:
            print "[!] Detected: Magento styles.css: " + websiteToScan + '/skin/frontend/default/default/css/styles.css'
       # else:
       #     print " |  Not Detected: Magento styles.css: " + websiteToScan + '/skin/frontend/default/default/css/styles.css'

        mag404Check = get(websiteToScan + '/errors/design.xml')
        if mag404Check.status_code == 200 and "magento" in mag404Check.text:
            print "[!] Detected: Magento error page design.xml: " + websiteToScan + '/errors/design.xml'
       # else:
       #     print " |  Not Detected: Magento error page design.xml: " + websiteToScan + '/errors/design.xml'

        ####################################################
        # Drupal Scans
        ####################################################

        print
        #print "[+] Running the Drupal scans..."

        drupalReadMeCheck = get(websiteToScan + '/readme.txt')
        if drupalReadMeCheck.status_code == 200 and 'drupal' in drupalReadMeCheck.text and '404' not in drupalReadMeCheck.text:
            print "[!] Detected: Drupal Readme.txt: " + websiteToScan + '/readme.txt'
      #  else:
      ##      print " |  Not Detected: Drupal Readme.txt: " + websiteToScan + '/readme.txt'

        drupalTagCheck = get(websiteToScan)
        if drupalTagCheck.status_code == 200 and 'name="Generator" content="Drupal' in drupalTagCheck.text:
            print "[!] Detected: Generated by Drupal tag on index"
      #  else:
        #    print " |  Not Detected: Generated by Drupal tag on index"

        drupalCopyrightCheck = get(websiteToScan + '/core/COPYRIGHT.txt')
        if drupalCopyrightCheck.status_code == 200 and 'Drupal' in drupalCopyrightCheck.text and '404' not in drupalCopyrightCheck.text:
            print "[!] Detected: Drupal COPYRIGHT.txt: " + websiteToScan + '/core/COPYRIGHT.txt'
       # else:
       #     print " |  Not Detected: Drupal COPYRIGHT.txt: " + websiteToScan + '/core/COPYRIGHT.txt'

        drupalReadme2Check = get(websiteToScan + '/modules/README.txt')
        if drupalReadme2Check.status_code == 200 and 'drupal' in drupalReadme2Check.text and '404' not in drupalReadme2Check.text:
            print "[!] Detected: Drupal modules/README.txt: " + websiteToScan + '/modules/README.txt'
        #else:
       #     print " |  Not Detected: Drupal modules/README.txt: " + websiteToScan + '/modules/README.txt'

        drupalStringCheck = get(websiteToScan)
        if drupalStringCheck.status_code == 200 and 'drupal' in drupalStringCheck.text:
            print "[!] Detected: Drupal strings on index"
        #else:
         #   print " |  Not Detected: Drupal strings on index"

        ####################################################
        # phpMyAdmin Scans
        ####################################################

        print
        #print "[+] Running the phpMyAdmin scans..."

        phpMyAdminCheck = get(websiteToScan)
        if phpMyAdminCheck.status_code == 200 and 'phpmyadmin' in phpMyAdminCheck.text:
            print "[!] Detected: phpMyAdmin index page"
     #   else:
      #  #    print " |  Not Detected: phpMyAdmin index page"

        pmaCheck = get(websiteToScan)
        if pmaCheck.status_code == 200 and 'pmahomme' in pmaCheck.text or 'pma_' in pmaCheck.text:
            print "[!] Detected: phpMyAdmin pmahomme and pma_ style links on index page"
      #  else:
        #    print " |  Not Detected: phpMyAdmin pmahomme and pma_ style links on index page"

        phpMyAdminConfigCheck = get(websiteToScan + '/config.inc.php')
        if phpMyAdminConfigCheck.status_code == 200 and '404' not in phpMyAdminConfigCheck.text:
            print "[!] Detected: phpMyAdmin configuration file: " + websiteToScan + '/config.inc.php'
      #  else:
      #      print " |  Not Detected: phpMyAdmin configuration file: " + websiteToScan + '/config.inc.php'

       # print
       # print "Scan is now complete!"
       # print

scan()

