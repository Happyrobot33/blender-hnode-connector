from bthl.util.general import scale_number

def getPositionAsDMX(loc, range, bytesPerAxis=1) -> bytearray:
    xscale = int(scale_number(loc.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(loc.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(loc.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = xscale.to_bytes(bytesPerAxis, byteorder='big')
    ybytes = yscale.to_bytes(bytesPerAxis, byteorder='big')
    zbytes = zscale.to_bytes(bytesPerAxis, byteorder='big')
    return bytearray(xbytes + ybytes + zbytes)

def getRotationAsDMX(rot, range, bytesPerAxis=1) -> bytearray:
    xscale = int(scale_number(rot.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(rot.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(rot.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = xscale.to_bytes(bytesPerAxis, byteorder='big')
    ybytes = yscale.to_bytes(bytesPerAxis, byteorder='big')
    zbytes = zscale.to_bytes(bytesPerAxis, byteorder='big')
    return bytearray(xbytes + ybytes + zbytes)

def getQuaternionAsDMX(rot, range, bytesPerAxis=1) -> bytearray:
    xscale = int(scale_number(rot.x, 0, (2**(8*bytesPerAxis))-1, -range, range))
    yscale = int(scale_number(rot.y, 0, (2**(8*bytesPerAxis))-1, -range, range))
    zscale = int(scale_number(rot.z, 0, (2**(8*bytesPerAxis))-1, -range, range))
    wscale = int(scale_number(rot.w, 0, (2**(8*bytesPerAxis))-1, -range, range))
    #now convert to bytes
    xbytes = xscale.to_bytes(bytesPerAxis, byteorder='big')
    ybytes = yscale.to_bytes(bytesPerAxis, byteorder='big')
    zbytes = zscale.to_bytes(bytesPerAxis, byteorder='big')
    wbytes = wscale.to_bytes(bytesPerAxis, byteorder='big')
    return bytearray(xbytes + ybytes + zbytes + wbytes)

def getColorAsDMX(color):
    r = int(scale_number(color[0], 0,255,0,1))
    g = int(scale_number(color[1], 0,255,0,1))
    b = int(scale_number(color[2], 0,255,0,1))
    return bytes([r, g, b])
