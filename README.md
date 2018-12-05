# TheXFramework
Network/WebApplication Information Gathering, Enumeration and Vulnerability Scanning
## Xframework Dark 
- Network Scanner  
  - Network Scanning For Open/Filter Ports 
- X-Attacker Core 
  - Information Gathering
  - CMS Identifier (More Than 120 CMS)
  - WAF Testing (Enumeration, Limited Firewall Bypass Recommendation) 
  - CMS-ENUMERATION For Drupal/Wordpress/Joomla/Vb
  - Crawler For URL with Parameters
  - LFI, RFI, and RCE
  - Sql-injection 
  - Template-Injection 
  - Basic XSS Check
  - CSRF Scan 
  - Brute force directories and files in websites
  
### What Tools It You Can Use in TheXFramework ?

- Nmap 
- Raccoon
- NSE Scripts 
- Golismero and Golismero Plugin Nikto
- CMSmap/WPScan/WPsecu/Droopscan/Joomscan [CMS Attacks]
- Photon 
- Crawler Engine
- Sqlmap 
- Tplmap 
- Sqliv 
- XssPy 
- Xsstrick
- Bunch of Other Scrpits/Tools

### Installation 
(Soon) 

### Usage 

    usage: ./xframework.py -u <Target> [Options/Scans]

    optional arguments:
      -h, --help         show this help message and exit

    Required Options:
      -u URL, --url URL  root url

    Options:
      -v, --verbose      Verbose Mode
      -b, --batch        batch Mode
      -F, --fast         Run Very Fast Without Logging/Saving/History [Soon]
    Scans:
      --banner           Grab Target Banner
      --wafbanner        Agressive Banner Grabbing with Limited WAF detection
      --wafstress        Web Application Firewall Stress(Optional : Fuzzfile)
      --waf              Web ApplicationFirewall and Server Service Detection
      --cms              CMS Identifier
      --lfi              Local File Inclution Attack (Optional : Fuzzfile)
      --clickjack        clickjack Vuln Scan
      --tempi            Template Injection Attack
      --sqlimini         Pre-Enumeration Simple Sqli Attacks
      --sqliv            Enumeration Simple Sqli Attacks
      --sqlmap           Identify Databases with Sqlmap
      --sqlmapdump       Identify Databases with Sqlmap
      --xssmini          Pre-Enumeration Simple Cross Siting Scripting
      --xsspy            Pre-Enumeration Simple Cross Siting Scripting
      --drupal           Droopal Full Enumeration
      --wordpress        Wordpress Full Enumeration with wpscan
      --wordpress2       Wordpress Full Enumeration with wpseku
      --joomla           Joomla Full Enumeration with wpseku
      --golismero        Target Full Enumeration with golismero
      --raccoon          Raccoon Framework Full Scan
      --shellshock       Scan For shellshock
      --xssstrick        Scan a URL For XSS injection with XSS-Strick

    Crawler Engine:
      --crawler          Run Crawler
      --deep             Run Crawler With Deep Depth
      --photon           Run Crawler With Minimized Photon Engine
      --photonold        Run Crawler With Photon Engine


### What Is Under Development and What is The Future ? 
This Options Are Under Development But They will be added to Version 2 of TXF 
 - Auto Network Port Scanner
 - Auto web Application Scanner
 - Threading
 - Plugin Engine

To Add In Future : 
  - Metasploit
  - Zmap
  - wapiti / WAFW00F / Commix
