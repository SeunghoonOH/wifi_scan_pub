#!/usr/bin/env python
# license removed for brevity


import rospy
#import rssi
from rssi import RSSI_Scan #Imports the RSSI_scan class from the sibling rssi file
from rssi import RSSI_Localizer


from wifi_scan_pub.msg import AddressRSSI
from wifi_scan_pub.msg import Fingerprint



def all_access_pt(raw_info):
    msg = Fingerprint()
    raw_cells = raw_info.split('Cell')
    raw_cells.pop(0) # Remove unneccesary "Scan Completed" message.
    if(len(raw_cells) > 0): # Continue execution, if atleast one network is detected.
            # Iterate through raw cells for parsing.
            # Array will hold all parsed cells as dictionaries.
    	#formatted_cells = [parseFPCell(cell) for cell in raw_cells]
        for cell in raw_cells:
            mac_sig_info = AddressRSSI()
	    mac_sig_info.address = getMACADD(cell)
            mac_sig_info.rssi = getSignalLevel(cell)
	    msg.list.append(mac_sig_info)
            # Return array of dictionaries, containing cells.
    	return msg
    else:
    	print("Networks not detected.")
    	return False


def getMACADD(raw_cell):
    ssid = raw_cell.split('Address: ')[1]
    ssid = ssid.split(' ')[0]
    return ssid


def getQuality(raw_cell):
    quality = raw_cell.split('Quality=')[1]
    quality = quality.split(' ')[0]
    return quality


def getSignalLevel(raw_cell):
    signal = raw_cell.split('Signal level=')[1]
    signal = int(signal.split(' ')[0])
    return signal


def parseFPCell(raw_cell):
    cell = {
    	'ssid': getMACADD(raw_cell),
    	'quality': getQuality(raw_cell),
    	'signal': getSignalLevel(raw_cell)
	}
    return cell



def wifi_scan():

    rospy.init_node('wifi_scan_node', anonymous=True)
    interface = rospy.get_param('~interface', 'wlx88366cfc5e50')
    wifi_topic = rospy.get_param('topic','wifi_fp')
    pub = rospy.Publisher(wifi_topic, Fingerprint, queue_size=10)
    rssi = RSSI_Scan(interface)
  

    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():

	 raw_scan_info = rssi.getRawNetworkScan(sudo=True)['output'] 
	 msg = all_access_pt(raw_scan_info)
	 if msg == False:
	 	continue
		
        # rospy.loginfo(msg)
         pub.publish(msg)

         rate.sleep()

if __name__ == '__main__':
    try:
        wifi_scan()
    except rospy.ROSInterruptException:
        pass

