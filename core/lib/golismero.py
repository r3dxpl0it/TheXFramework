from core.__import__ import r3dexecute

def golismero_scan(target) : 
		r3dexecute(['golismero -e dns_malware scan' + " " + 	target] , "[GOLISMERO][dns malware]") 
		r3dexecute(['golismero -e sqlmap scan' + " " + 	target] , "[GOLISMERO][Sqlmap]") 
		r3dexecute(['golismero -e nikto scan' + " " + 	target] , "[GOLISMERO][nikto]") 
		r3dexecute(['golismero -e zone_transfer scan' + " " + 	target] , "[GOLISMERO][zone_transfer]") 
		r3dexecute(['golismero -e brute_url_predictables scan' + " " + 	target] , "[GOLISMERO][URL Predictable BruteForce]") 
		r3dexecute(['golismero -e brute_dns scan' + " " + 	target] , "[GOLISMERO] [Dns BruteForse]") 
		r3dexecute(['golismero -e heartbleed scan' + " " + 	target] , "[GOLISMERO][Heartbleed]")
