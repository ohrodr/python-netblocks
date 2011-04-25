class Block(object):
      """
      This is the netblock object.  It represents and has all the required
      information of a netblock.
      """
      def __init__(self,cidr):
          from math import floor
          import re,sys
          cidr_regex = re.compile('^(\d+\.\d+\.\d+\.\d+)/(\d+)$')
          try:
                self.base  = str2pack(cidr_regex.match(cidr).group(1))
                self.bits  = int(cidr_regex.match(cidr).group(2))
          except:
                print "Give a valid CIDR."
          else:
                self.netmask = netmask(self.bits)
                self.network = network(self.base,self.netmask)
                self.broadcast = broadcast(self.base,self.netmask,self.bits)
                self.usable = usable(self.bits)
                self.inverse = ( ~ netmask(self.bits) & 0xFFFFFFFF)
      def __repr__(self):
        return pack2str(self.base) + '/' + str(self.bits)
      
      def nextblock(self,index=1):
        """
        this method will return the next possible netblock
        """
        oldblock = self.network
        bits = self.bits
        newblock = oldblock + index * (2**(32-bits))
        b = Block(pack2sstr(newblock) + '/' + str(bits))
        if b.network >= 2**32:
              return False
        if b.network < 0:
              return False
        return b
      
      def inblock(self,ip):
          """
          returns True if the ip given as a str()
          is in the netblock passed from Block() class
          """
          if ip & self.netmask == self.network:
             return True
          else:
             return False

def netmask(bits):
    """
    given x bits return the netmask.
    """
    y = 0
    for i in xrange(32-bits,32):
          y |= (1 << i )
    return y

def pack2str(invar):
    """
    This is the reverse of str2pack.
    it will take a long integer and return the IP address.
    """
    import struct,socket
    return socket.inet_ntoa(struct.pack('!L',invar))

def str2pack(invar):
    """
    This is rodr's ghetto fabulous ip address -> integer conversion
    """
    import struct,socket
    return struct.unpack("!L",socket.inet_aton(invar))[0]

def network(ip,subnet):
    """
    given an ip and subnet as long int return the network address
    """
    return ip & subnet

def broadcast(ip,subnet,bits):
    """
    given an ip, subnet and bits return the broadcast address.
    """
    return (ip & subnet) + 2**(32-bits)-1

def usable(bits):
    """
    given the bits of a network count usable addresses
    """
    return 2**(32-bits)-2

def maxblock(network,bits=32):
    """
    given a network address this method will let you know the maximum size 
    of that netblock. for example: 10.24.2.0 alone could be a /23 ->/32
    """
    while (bits > 0):
          mask = netmask(bits-1)
          if (network & mask) != network:
                 #bits = bits-1
                 break 
          else:
                 bits = bits-1
    return bits

def range2cidr(start,end):
  """
  given a startip and end ip this will return a list
  of all the netblocks that span that range
  """
      from math import floor,log
      s = start.base
      e = end.base
      result = []
      while ( e >= s):
            maxsize = maxblock(s,32)
            maxdiff = int(32 - floor(log(e - s + 1)/log(2)))
            if maxsize < maxdiff:
                  maxsize = maxdiff
            result.append(Block(pack2str(s) + '/' + str(int(maxsize))))
            s += 2**(32-maxsize)
      return result
