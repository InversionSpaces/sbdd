def SBDHandle(binary, payload=None):
    from struct import unpack as un
    from struct import calcsize as calc
    from binascii import hexlify as hexy
    
    protover = un(">B", binary[:1])[0]
    if(protover != 1):
        print("Protocol Mismatch")
        return
    
    overalllen = un(">h", binary[1:3])[0]
    if(overalllen + 3 != len(binary)):
        print("Size Mismatch")
        return
        
    res = {"MOHeader" : list(), 
           "MOLocationInformation" : list(),
           "MOPayload" : list()}
    
    carret = 3
    while(carret != overalllen + 3):
        iei = un(">B", binary[carret : carret + 1])[0]
        carret += 1
        
        lng = un(">h", binary[carret : carret + 2])[0]
        carret += 2
        
        if(iei == 1):
            fields = ("CDRReference", "IMEI", "SessionStatus", 
            "MOMSN", "MTMSN", "TimeOfSession")
            fmt = ">I15sB2HI"
            case = "MOHeader"
        
        elif(iei == 2):
            if(payload):
                fields, fmt = payload
                
            else:
                fields = ("Payload",)
                fmt = "{}s".format(lng) 
        
            case = "MOPayload"
            
        elif(iei == 3):
            fields = ("Indicator", "LatitudeDegrees","LatitudeThousandthsOfMinute", 
                "LongitudeDegrees", "LongitudeThousandthsOfMinute", "CEPRadius")
            fmt = ">cBHBHI"
            case = "MOLocationInformation"
        
        else:
            print("IEI Mismatch")
            return
        
        size = calc(fmt)
        count = lng / size
        
        if(count % 1 != 0):
            print("Size Mismatch")
            return
        
        for i in range(int(count)):
            data = list(un(fmt, binary[carret + i*size: carret + (i + 1)*size]))
            
            for index, item in enumerate(data):
                if(isinstance(item, bytes)):
                    data[index] = item.hex()
            
            res[case].append(dict(zip(fields, data))) 
        
        carret += lng
    
    return res


