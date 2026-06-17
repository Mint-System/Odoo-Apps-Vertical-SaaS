import hashlib

## Version detection
def get_ocad_checksum(v, lnum, e, lname):
    if v == 2018:
        return get_ocad2018_checksum(v, lnum, e, lname)
    elif v == 12:
        return get_ocad12_checksum(v, lnum, e, lname)
    elif v == 11:
        return get_ocad11_checksum(v, lnum, e, lname)
    elif v == 10:
        return get_ocad10_checksum(v, lnum, e, lname)
    else:
        return list('xxxxxxxxxx')


## Helper functions
# Get hash string
def hash_of_string(s):
    return hashlib.sha1(s.encode("utf-16-le")).hexdigest().upper()


# Convert hex to integer
def hex_to_int(s):
    hx = 0
    s = s.upper()
    slist = list(s)
    for c in slist:
        hx = hx * 16
        if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            hx = hx + ord(c) - ord("0")
        else:
            hx = hx + ord(c) - ord("A") + 10
        # print(c+" .. "+ str(hx)  +"--- "+ str(ord(c)) )
    return hx


def uppercase(oldStr: str):
    newStr = ""
    for c in oldStr:
        if "a" <= c <= "z":
            newStr += chr(ord(c) - 32)
        else:
            newStr += c
    return newStr


# Get key byte
def pkv_get_key_byte(seed, a, b, c):
    a = a % 25
    b = b % 3
    if a % 2 == 0:
        return (((seed >> a) & 0x000000FF) ^ ((seed >> b) | c)) & 0x000000FF
    else:
        return (((seed >> a) & 0x000000FF) ^ ((seed >> b) & c)) & 0x000000FF


def IntToCodeOcad11CourseSetting(i):
    i = i % 33
    charTableOcad11 = 'Q15TH9AY4C6U2WZS8MPX3FGJ7DKLBVNRE'
    return charTableOcad11[i]


def IntToCodeOcad11Starter(i):
    i = i % 33
    charTableOcad11 = 'D1N49A5HB7J8GMF2WXEUTK3LCZPQRSV6Y'
    return charTableOcad11[i]


def IntToCodeOcad11OrienteeringStandard(i):
    i = i % 33
    charTableOcad11 = 'F9WZJMCBLT4QXDRN8HAU25KSY3E6P7VG1'
    return charTableOcad11[i]


def IntToCodeOcad11Professional(i):
    i = i % 33
    charTableOcad11 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
    return charTableOcad11[i]


def IntToCodeOcad10Cs(i):
    i = i % 31
    charTableOcad10 = ('2','3','4','5','6','7','8','9', 'A','B','C','D','E','F','G','H','J', 'K','L','M','N','P','R','S','T', 'U','V','W','X','Y','Z')
    return charTableOcad10[i]


def IntToCodeOcad10Std(i):
    i = i % 31
    charTableOcad10 = ( '2','3','4','5','6','7','8','9', 'A','B','C','D','E','F','G','H','J', 'K','L','M','N','P','R','S','T', 'U','V','W','X','Y','Z')
    return charTableOcad10[i]


def IntToCodeOcad10Pro(i):
    i = i % 33
    charTableOcad10 = ( '1','2','3','4','5','6','7','8','9', 'A','B','C','D','E','F','G','H','J', 'K','L','M','N','P','Q','R','S','T', 'U','V','W','X','Y','Z')
    return charTableOcad10[i]


## Checksum generation
# Get OCAD2018 checksum
def get_ocad2018_checksum(v, lnum, e, lname):
    slist = list(e)
    checksum = list("____-____-____")

    for i in [5, 6, 7, 8, 10, 11]:
        slist = list(hash_of_string("".join(slist).upper() + uppercase(lname) + str(lnum) + uppercase(lname)))
        # print(''.join(slist))
        idx = (v * (i + 1) + lnum) % 40
        # print(idx)
        checksum[i] = slist[idx]

    # print(checksum)

    s = checksum[5] + checksum[6] + checksum[7] + checksum[8] + checksum[10] + checksum[11]
    # print(s)
    a = pkv_get_key_byte(hex_to_int(s), lnum % 256, v % 2000, 13)
    # a = pkv_get_key_byte(8406981, ln % 256, v % 2000, 13)
    sl = list(f"{a:02X}")
    checksum[12] = sl[0]
    checksum[13] = sl[1]
    # print(checksum)

    s = "".join(checksum).replace("_", "")
    s = s.replace("-", "")

    slist = list(s)
    # print(s)

    slist = list(hash_of_string(e + "".join(slist).upper() + str(lnum) + uppercase(lname)))
    checksum[0] = slist[8]
    checksum[1] = slist[23]
    checksum[2] = slist[12]
    checksum[3] = slist[16]
    # print(checksum)
    return checksum


# Get OCAD 12 checksum
def get_ocad12_checksum(v, lnum, e, lname):     
        
    if (e == 'Academic'):
        e = 'Mapping Solution'    
    
    slist = list(e)
    checksum = list('____-____-____')
    for i in [5, 6, 7, 8, 10, 11]:
        slist = list(hash_of_string(''.join(slist).upper() + str(lnum) + lname.upper()))
        #print(''.join(slist))
        idx = (v * (i + 1) + lnum) % 40
        #print(idx)
        checksum[i] = slist[idx]
        
    #print(checksum)

    s = checksum[5] + checksum[6] + checksum[7] + checksum[8] + checksum[10] + checksum[11]
    #print(s)
    a = pkv_get_key_byte(hex_to_int(s), lnum % 256, v, 89)
    sl = list('{0:02X}'.format(a))
    checksum[12] = sl[0]
    checksum[13] = sl[1]
    #print(checksum)

    s = ''.join(checksum).replace('_', '')
    s = s.replace("-", "")

    slist = list(s)
    #print(s)

    slist = list(hash_of_string(e + ''.join(slist).upper() + str(lnum) + lname.upper()))
    checksum[0] = slist[7]
    checksum[1] = slist[22]
    checksum[2] = slist[11]
    checksum[3] = slist[17]
    #print(checksum)
    return checksum


# Get OCAD 11 checksum
def get_ocad11_checksum(v, lnum, e, lname):

    maxUint32 = 4294967296;
    
    if (e == 'Academic'):
        e = 'Professional'    
    
    slist = list('__________')

    s = ""
    iSum = 0;
    factor = 0

    if (e == "Course Setting"):
        s =  ('FkHze9dDs2' + lname + 'gd5' + str(lnum)).upper()
        iSum = lnum + 891
        factor = 15
    elif (e == "Starter"):
        s =  ('jedzsT89s0' + lname + 'nR7sW' + str(lnum)).upper()
        iSum = lnum + 780
        factor = 23
    elif (e == "Orienteering Standard"):
        s =  ('H8D7shE' + lname + 'DmnDu7S534' + str(lnum)).upper()
        iSum = lnum - 23
        factor = 18
    elif (e == "Professional"):
        s =  ('ajtiEjt' + lname + 'jR5d3s' + str(lnum)).upper()
        iSum = lnum - 783
        factor = 19

    # print(s)
    # print(iSum)
    # print(factor)
       
    for item in s:
        if ((item >= 'A') and (item <= 'Z')) or ((item >= '0') and (item <= '9')):
            iSum = ((((iSum + factor) % maxUint32 * factor) % maxUint32) * (ord(item)+9)) % maxUint32;
            factor += 3

    if (iSum < 200000):
        iSum = iSum + 200000;
    iLicenseShort = lnum % 1000;

    #Prepare checksum
    if (e == "Course Setting"):
        slist[0] = IntToCodeOcad11CourseSetting((iSum // 79) % 32)
        slist[1] = IntToCodeOcad11CourseSetting((iSum // 642) % 31);
        slist[2] = IntToCodeOcad11CourseSetting(((iLicenseShort*221) // 79) % 32);
        slist[3] = IntToCodeOcad11CourseSetting((iSum // 978) % 31);
        slist[4] = IntToCodeOcad11CourseSetting(((iLicenseShort*7811) // 6) % 28);
        slist[5] = IntToCodeOcad11CourseSetting((iSum // 175) % 28);
        slist[6] = IntToCodeOcad11CourseSetting((iSum // 279) % 27);
        slist[7] = IntToCodeOcad11CourseSetting(((iLicenseShort*897) // 47) % 27);
        slist[8] = IntToCodeOcad11CourseSetting(((iLicenseShort*459) // 40) % 28);
        slist[9] = IntToCodeOcad11CourseSetting((iSum // 345) % 31);
    elif (e == "Starter"):
        slist[0] = IntToCodeOcad11Starter((iSum // 59) % 31);
        slist[1] = IntToCodeOcad11Starter((iSum // 978) % 27);
        slist[2] = IntToCodeOcad11Starter((iSum // 698) % 30);
        slist[3] = IntToCodeOcad11Starter(((iLicenseShort*25) // 6) % 30);
        slist[4] = IntToCodeOcad11Starter(((iLicenseShort*78) // 47) % 27);
        slist[5] = IntToCodeOcad11Starter((iSum // 472) % 28);
        slist[6] = IntToCodeOcad11Starter(((iLicenseShort*181) // 709) % 29);
        slist[7] = IntToCodeOcad11Starter((iSum // 781) % 30);
        slist[8] = IntToCodeOcad11Starter((iSum // 79) % 28);
        slist[9] = IntToCodeOcad11Starter(((iLicenseShort*57) // 40) % 31);
    elif (e == "Orienteering Standard"):
        slist[0] = IntToCodeOcad11OrienteeringStandard((iSum // 268) % 27);
        slist[1] = IntToCodeOcad11OrienteeringStandard(((iLicenseShort*65) // 47) % 27);
        slist[2] = IntToCodeOcad11OrienteeringStandard((iSum // 842) % 28);
        slist[3] = IntToCodeOcad11OrienteeringStandard(((iLicenseShort*57) // 40) % 31);
        slist[4] = IntToCodeOcad11OrienteeringStandard(((iLicenseShort*21) // 709) % 29);
        slist[5] = IntToCodeOcad11OrienteeringStandard((iSum // 98) % 30);
        slist[6] = IntToCodeOcad11OrienteeringStandard(((iLicenseShort*721) // 6) % 30);
        slist[7] = IntToCodeOcad11OrienteeringStandard((iSum // 79) % 28);
        slist[8] = IntToCodeOcad11OrienteeringStandard((iSum // 95) % 30);
        slist[9] = IntToCodeOcad11OrienteeringStandard((iSum // 597) % 31);
    elif (e == "Professional"):
        slist[0] = IntToCodeOcad11Professional((iSum // 259) % 27);
        slist[1] = IntToCodeOcad11Professional(((iLicenseShort*5) // 47) % 27);
        slist[2] = IntToCodeOcad11Professional((iSum // 6842) % 28);
        slist[3] = IntToCodeOcad11Professional(((iLicenseShort*587) // 40) % 31);
        slist[4] = IntToCodeOcad11Professional(((iLicenseShort*121) // 709) % 29);
        slist[5] = IntToCodeOcad11Professional((iSum // 958) % 30);
        slist[6] = IntToCodeOcad11Professional(((iLicenseShort*7211) // 6) % 30);
        slist[7] = IntToCodeOcad11Professional((iSum // 779) % 28);
        slist[8] = IntToCodeOcad11Professional((iSum // 985) % 30);
        slist[9] = IntToCodeOcad11Professional((iSum // 97) % 31);
    return slist


# Get OCAD10 checksum
def get_ocad10_checksum(v, lnum, e, lname):     

    maxUint32 = 4294967296;

    if (e == 'Academic'):
        e = 'Professional'    
    
    slist = list('__________')

    s = ""
    iSum = 0;
    factor = 0;

    if (e == "Course Setting"):
        lnum = lnum % 100000;
        s =  'ABC' + lname.upper() + 'GHUSR' + str(lnum) + 'GSR'
        iSum = lnum - 656
        factor = 3
                  
        for item in s:
            if ((item >= 'A') and (item <= 'Z')) or ((item >= '0') and (item <= '9')):
                iSum = ((((iSum + factor) % maxUint32 * factor) % maxUint32) * (ord(item)+6)) % maxUint32;
                factor += 4

        if (iSum < 200000):
            iSum = iSum + 200000;

        slist[0] = IntToCodeOcad10Cs((iSum // 259) % 27);
        slist[1] = IntToCodeOcad10Cs(((lnum*587) // 40) % 31);
        slist[2] = IntToCodeOcad10Cs(((lnum*5) // 47) % 27);
        slist[3] = IntToCodeOcad10Cs((iSum // 6842) % 28);
        slist[4] = IntToCodeOcad10Cs(((lnum*121) // 709) % 29);
        slist[5] = IntToCodeOcad10Cs((iSum // 958) % 30);
        slist[6] = IntToCodeOcad10Cs(((lnum*7211) // 6) % 30);
        slist[7] = IntToCodeOcad10Cs((iSum // 779) % 28);
        slist[8] = IntToCodeOcad10Cs((iSum // 985) % 30);
        slist[9] = IntToCodeOcad10Cs((iSum // 98) % 31);
    elif (e == "Orienteering Standard"):
        s =  'FRG' + lname.upper() + 'FGZE' + str(lnum)
        iSum = lnum - 28
        factor = 13

        for item in s:
            if ((item >= 'A') and (item <= 'Z')) or ((item >= '0') and (item <= '9')):
                iSum = ((((iSum + factor) % maxUint32 * factor) % maxUint32) * (ord(item)+9)) % maxUint32;
                factor += 3

        if (iSum < 200000):
            iSum = iSum + 200000;             

        slist[0] = IntToCodeOcad10Std((iSum // 412) % 30);
        slist[1] = IntToCodeOcad10Std(((lnum*685) // 47) % 27);
        slist[2] = IntToCodeOcad10Std(((lnum*6785) // 40) % 31);
        slist[3] = IntToCodeOcad10Std((iSum // 6794) % 28);
        slist[4] = IntToCodeOcad10Std((iSum // 7835) % 28);
        slist[5] = IntToCodeOcad10Std(((lnum*311) // 879) % 29);
        slist[6] = IntToCodeOcad10Std(((lnum*111) // 76) % 30);
        slist[7] = IntToCodeOcad10Std((iSum // 7137) % 31);
        slist[8] = IntToCodeOcad10Std((iSum // 59) % 30);
        slist[9] = IntToCodeOcad10Std((iSum // 849) % 31);
    elif (e == "Professional"):
        s =  str(lnum) + lname.upper()
        iSum = lnum + 29
        factor = 7

        for item in s:
            if ((item >= 'A') and (item <= 'Z')) or ((item >= '0') and (item <= '9')):
                iSum = ((((iSum + factor) % maxUint32 * factor) % maxUint32) * (ord(item)+4)) % maxUint32;
                factor += 2

        if (iSum < 100000):
            iSum = iSum + 100000;

        slist[0] = IntToCodeOcad10Pro((iSum // 74912) % 32);
        slist[1] = IntToCodeOcad10Pro(((lnum*685) // 47) % 27);
        slist[2] = IntToCodeOcad10Pro(((lnum*6785) // 40) % 33);
        slist[3] = IntToCodeOcad10Pro((iSum // 74912) % 32);
        slist[4] = IntToCodeOcad10Pro((iSum // 835) % 28);
        slist[5] = IntToCodeOcad10Pro((iSum // 7954) % 32);
        slist[6] = IntToCodeOcad10Pro(((lnum*111) // 76) % 30);
        slist[7] = IntToCodeOcad10Pro((iSum // 13) % 33);
        slist[8] = IntToCodeOcad10Pro((iSum // 729) % 19);
        slist[9] = IntToCodeOcad10Pro((iSum // 7749) % 33);
    return slist


# Version = OCAD 2018 Orienteering
# Name = OL Ishikawa
# Number = 19277
# Checksum = BB83-215D-EE94
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=19277&v=2018&d=un8ifnoj

checksum = "".join(
    get_ocad_checksum(
        2018,
        int("19277"),
        "Orienteering",
        "OL Ishikawa",
    )
)
print(checksum)
print("BB83-215D-EE94" == checksum)

# Version = OCAD 2018 Orienteering
# Name = OL Ishikawa
# Number = 19278
# Checksum = C130-69AF-D0FA
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=19278&v=2018&d=v78pM3ZH

checksum = "".join(
    get_ocad_checksum(
        2018,
        int("19278"),
        "Orienteering",
        "OL Ishikawa",
    )
)
print(checksum)
print("C130-69AF-D0FA" == checksum)

# Version = OCAD 2018 Orienteering
# Name = Tsukuba44comp
# Number = 25664
# Checksum = 6E9D-030B-ADA1
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=25664&v=2018&d=hhXX9wux

checksum = "".join(
    get_ocad_checksum(
        2018,
        int("25664"),
        "Orienteering",
        "Tsukuba44comp",
    )
)
print(checksum)
print("6E9D-030B-ADA1" == checksum)

# Version = OCAD 2018 Orienteering
# Name = Tsukuba44comp
# Number = 25665
# Checksum = 743D-1013-5624
# Download link = https://www.ocad.com/OCAD2018/OCAD_2018_Setup.php?e=ORI&l=25665&v=2018&d=LYZ39ruh

checksum = "".join(
    get_ocad_checksum(
        2018,
        int("25665"),
        "Orienteering",
        "Tsukuba44comp",
    )
)
print(checksum)
print("743D-1013-5624" == checksum)

# Name = Långhundra IF
# Number = 5323
# Checksum Admin = 8EF8-7CFA-3E4B

checksum = "".join(
    get_ocad_checksum(
        2018,
        int("5323"),
        "Orienteering",
        "Långhundra IF",
    )
)
print(checksum)
print("8EF8-7CFA-3E4B" == checksum)

# Name = FHNW - Schulungslizenz
# Number = 14479
# Edition = Academic
# Checksum Admin = 0E37-AAC6-3A15

checksum = "".join(
    get_ocad_checksum(
        2018,
        int("14479"),
        "Academic",
        "FHNW - Schulungslizenz",
    )
)
print(checksum)
print("0E37-AAC6-3A15" == checksum)

# Name = HSOK
# Number = 26305
# Edition = Orienteering
# Checksum Admin = 3967-6964-E2F5

checksum = "".join(
    get_ocad_checksum(
        2018,
        int("26305"),
        "Orienteering",
        "HSOK",
    )
)
print(checksum)
print("3967-6964-E2F5" == checksum)

for test_input in [
    [12, 2005902, 'Course Setting', 'OCAD AG', "4C1C-EE08-9166"],
    [12, 9795, 'Orienteering', 'Wimberley and Associates', "2D1D-0532-0703"],
    [12, 5002, 'Mapping Solution', 'OCAD AG', "476A-FB45-8ED2"],
    [12, 5002, 'Professional', 'OCAD AG', "D79A-7BFF-669F"],
    [12, 5002, 'Orienteering', 'OCAD AG', "4EB2-9F2F-F8A1"],
    [12, 5002, 'Starter', 'OCAD AG', "3089-594E-20CA"],
    [11, 5002, 'Professional', 'OCAD AG', "T18W164MG2"],
    [11, 5003, 'Orienteering Standard', 'OCAD AG', "RJNJFHFTYM"],
    [11, 15023, 'Starter', '35 RAP', "FPWA8FA9C1"],
    [11, 2005902, 'Course Setting', 'OCAD AG', "LYLAML1SPL"],
    [10, 5002, 'Professional', 'OCAD AG', "9229AFG57L"],
    [10, 5003, 'Orienteering Standard', 'OCAD AG', "RJARA3KZ5W"],
    [10, 2005902, 'Course Setting', 'OCAD AG', "VX84UPN6R9"],
    [1, 2005902, 'Course Setting', 'OCAD AG', "xxxxxxxxxx"],
]:
    checksum = "".join(get_ocad_checksum(*test_input[:4]))
    expected_checksum = test_input[4]
    print(checksum)
    print(checksum == expected_checksum)