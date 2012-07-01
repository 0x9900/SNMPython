'''
@author: Carl Verge
@contact: carlverge@gmail.com
@version: 12.06
@requires: Python 2.6, net-snmp python bindings
@warning: No warranty or support included. Please don't call me if this nukes your node (send me a picture, though!)
'''

import netsnmp
from collections import namedtuple


class SNMPError(Exception):
    '''
    The base error for all other SNMP errors in this module. If you catch this exception, it will include all other SNMP errors.
    Contains the error string, and may contain the error number, index, and the failed varlist.
    @param errstring: Mandatory, the string returned from netsnmp for the error.
    @param errno: The SNMP error number. (Optional)
    @param errind: The index of the failing varbind in the varlist (Optional)
    @param varlist: The failed varlist. (Optional)
    '''
    def __init__(self, errstring, errno=None, errind=None, varlist=None):
        self.errstring = errstring
        self.errno = errno
        self.errind = errind
        self.varlist = varlist
        
    def __str__(self):
        error = ["%s " % self.errstring]
        if self.errno != None: error.append(" Error Number: %d" % self.errno)
        if self.errind != None: error.append(" Error Index: %d" % self.errind)
        return ''.join(error)


class SNMPTimeoutError(SNMPError):
        '''The SNMP Request Timed Out.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPTooBigError(SNMPError):
        '''The agent could not place the results of the requested SNMP operation in a single SNMP message.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
      
class SNMPNoSuchNameError(SNMPError):
        '''The requested SNMP operation identified an unknown variable.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
      
class SNMPBadValueError(SNMPError):
        '''The requested SNMP operation tried to change a variable but it specified either a syntax or value error.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
 
class SNMPReadOnlyError(SNMPError):
        '''The requested SNMP operation tried to change a variable that was not allowed to change, according to the community profile of the variable.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPGenErr(SNMPError):
        '''An error other than one of those listed here occurred during the requested SNMP operation.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPNoAccessError(SNMPError):
        '''The specified SNMP variable is not accessible.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
 
class SNMPWrongTypeError(SNMPError):
        '''The value specifies a type that is inconsistent with the type required for the variable.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPWrongLengthError(SNMPError):
        '''The value specifies a length that is inconsistent with the length required for the variable.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPWrongEncodingError(SNMPError):
        '''The value contains an Abstract Syntax Notation One (ASN.1) encoding that is inconsistent with the ASN.1 tag of the field.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPWrongValueError(SNMPError):
        '''The value cannot be assigned to the variable.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
 
class SNMPNoCreationError(SNMPError):
        '''The variable does not exist, and the agent cannot create it.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPInconsistentValueError(SNMPError):
        '''The value is inconsistent with values of other managed objects.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPResourceUnavailableError(SNMPError):
        '''Assigning the value to the variable requires allocation of resources that are currently unavailable.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
 
class SNMPCommitFailedError(SNMPError):
        '''No validation errors occurred, but no variables were updated.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPUndoFailedError(SNMPError):
        '''No validation errors occurred. Some variables were updated because it was not possible to undo their assignment.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPAuthorizationError(SNMPError):
        '''An authorization error occurred.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)

class SNMPNotWritableError(SNMPError):
        '''The variable exists but the agent cannot modify it.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
            
class SNMPInconsistentNameError(SNMPError):
        '''The variable does not exist; the agent cannot create it because the named object instance is inconsistent with the values of other managed objects.'''
        def __init__(self, errstring, errno=None, errind=None, varlist=None):
            SNMPError.__init__(self, errstring, errno, errind, varlist)
 
               

class SNMPythonSession(netsnmp.Session):
    '''
    @author: Carl Verge
    @contact: carlverge@gmail.com
    @version: 12.06
    @requires: Python 2.6, net-snmp python bindings
    
    An attempt at a more pythonic approach to SNMP for simple scripts. Uses the netsnmp bindings
    as a base (I wanted to see if it would make a perf. difference vs pure SNMP python libs).
    Many of the methods in this module require that MIBs are loaded in netsnmp to perform translations.
    
    To install net-snmp and python bindings (net-snmp is preinstalled on many *NIX)
        Debian/Ubuntu: apt-get install snmp libsnmp-python
        Others: I've had no issues installing the python bindings from source, goto:
            http://net-snmp.sourceforge.net/download.html
    
    To load some MIBs into netsnmp:
        1. Run net-snmp-config --default-mibdirs
        2. Place your mibs in one of the directories it outputs.
        3. Run net-snmp-config --snmpconfpath
        4. Place the following in snmp.conf (probably in /etc/snmp):
            mibs +ALL
        5. This will load all the MIBs in all the directories automatically.
    
    
    To start a session (v2):
        session = SNMPythonSession(DestHost='192.168.1.1', Community='private', Version=2)
        
    To start getting variables:
        print session['sysUpTime.0'] #Returns a single value
        print session['sysDescr.0 sysLocation.0'] #Returns a tuple
        
    To set variables:
        session['sysContact.0'] = 'Fred' #Sets a single value
        session['ifIndex.1 ifIndex.2 sysLocation.0'] = 2, 1, 'Closet' #Sets all three at once
    
    Checking for the existance of an object (usually for tables):
        if 'ifDescr.2' in session: ... #Returns true if that object exists (a get succeeds)
   
    
    Full get/getnext methods:
        There are full methods to perform get/getnext, example:
            print session.get_next_data('sysContact','sysLocation')
            print session.get_next_data_oids('sysContact','sysLocation')  

        The difference between the two is the second one returns the OID, index, value, and type:
            ('Closet', 'Fred')
            [('sysContact', '0', 'Closet', 'OCTETSTR'), ('sysLocation', '0', 'Fred', 'OCTETSTR')]
            

    Getting an entire table (uses getbulk): 
        tab = session.get_table('ifTable')
        #The table is a dictionary with the row indicies as keys. The row is a named tuple with the column names as identifiers:
        #Example: get the ifDescr of the interface with ifIndex 3:
        
        print tab['3'].ifDescr
        for index, column in tab.iteritems(): print index, ':', columns
        
        Example output:
            Ethernet 0/0
            3 : TableRow(ifIndex='37453824', ifDescr='Ethernet 0/0', ifType='6', ifMtu='1514', ...
            4 : TableRow(ifIndex='37421056', ifDescr='Ethernet 0/1', ifType='6', ifMtu='1514', ...
            ...
    
    Getting a subtree (uses getbulk):
        #This will return a list of tuples, an entry for each value under that OID.
        list = session.get_subtree_data_oids('ifTable')
        for entry in list: print entry
        
        Example output:
            ('.iso.org.dod.internet.mgmt.mib-2.interfaces.ifTable.ifEntry.ifIndex', '1', '1', 'INTEGER32')
            ('.iso.org.dod.internet.mgmt.mib-2.interfaces.ifTable.ifEntry.ifIndex', '2', '2', 'INTEGER32')
            ...
        
    Tips on creating a row:
        #Set the row status to 5 (createAndWait), then configure the other parameters
        session['vRtrMplsLspRowStatus.1.5 vRtrMplsLspAdminState.1.5 vRtrMplsLspName.1.5 vRtrMplsLspType.1.5'] = 5, 2, 'carltestMark3', 2
        #Once everything else is set, try to set the RowStatus to 1 (active).
        session['vRtrMplsLspRowStatus.1.5'] = 1 
    
    Tips on deleting a row:
        #Set the RowStatus to 6. Depending on the object, you sometimes need to shut it down first.
        session['vRtrMplsLspRowStatus.1.3'] = 6
     
    Error Handling:
        Most failures (including SNMP timeouts) will raise a specific error, that is a subclass of SNMPError. For example:
            try:
                print session['ifOperStatus.5']
            except SNMPTimeoutError:
                #Catch timeouts spefically
            except SNMPError:  
                #All other errors 
                
        The exception object will always have an error string, and typically the error number, error index, and failed varbind as variables.
        
        The session object also contains the values for the most recent errors codes:
            session.ErrorInd
            session.ErrorNum
            session.ErrorStr
        
        
    Misc Attributes:
        The session object has a few other misc. attributes:
            UseEnums : If set to 1, translate enum numbers to strings. I've had this crash python on me.
            UseLongNames : Return the fully qualified OID name instead of the leaf name.
            UseNumeric : Force disable translation of OID names. This breaks many methods.
    
    '''


    def __init__(self, *args, **kwargs):
        
        '''
        Create a new SNMP session to target host. Examples:
            (snmpv2) session = SNMPythonSession(DestHost='192.168.1.1', Community='private', Version=2)
        Please see netsnmp docs (or just look at the netsnmp binding source) for the other parameters. There are a lot.  
        
        By default, OID name translation is turned on (required by a lot of the methods)
        As well, enum translation is turned off (I've had it crash python on me a few times)
        '''
        netsnmp.Session.__init__(self, *args, **kwargs)
        self.UseNumeric = 0
        #@bug: Disabled for now, I've had enum parsing crash the netsnmp lib (and the python interpreter by extension)
        self.UseEnums = 0
    
    #Copied wholesale from Microsoft's site of all things
    ERROR_MAP = {
                1: SNMPTooBigError, #The agent could not place the results of the requested SNMP operation in a single SNMP message.
                2: SNMPNoSuchNameError, #The requested SNMP operation identified an unknown variable.
                3: SNMPBadValueError, #The requested SNMP operation tried to change a variable but it specified either a syntax or value error.
                4: SNMPReadOnlyError, #The requested SNMP operation tried to change a variable that was not allowed to change, according to the community profile of the variable.
                5: SNMPGenErr, #An error other than one of those listed here occurred during the requested SNMP operation.
                6: SNMPNoAccessError, #The specified SNMP variable is not accessible.
                7: SNMPWrongTypeError, #The value specifies a type that is inconsistent with the type required for the variable.
                8: SNMPWrongLengthError, #The value specifies a length that is inconsistent with the length required for the variable.
                9: SNMPWrongEncodingError, #The value contains an Abstract Syntax Notation One (ASN.1) encoding that is inconsistent with the ASN.1 tag of the field.
               10: SNMPWrongValueError, #The value cannot be assigned to the variable.
               11: SNMPNoCreationError, #The variable does not exist, and the agent cannot create it.
               12: SNMPInconsistentValueError, #The value is inconsistent with values of other managed objects.
               13: SNMPResourceUnavailableError, #Assigning the value to the variable requires allocation of resources that are currently unavailable.
               14: SNMPCommitFailedError, #No validation errors occurred, but no variables were updated.
               15: SNMPUndoFailedError, #No validation errors occurred. Some variables were updated because it was not possible to undo their assignment.
               16: SNMPAuthorizationError, #An authorization error occurred.
               17: SNMPNotWritableError, #The variable exists but the agent cannot modify it.
               18: SNMPInconsistentNameError #The variable does not exist; the agent cannot create it because the named object instance is inconsistent with the values of other managed objects.          
               }
    
    def raise_error(self, errstring, errno=None, errind=None, varlist=None):
        #I have no idea why it sets errind to -24 for timeouts, but it does.
        if errind == -24: raise SNMPTimeoutError(errstring, errno, errind, varlist)
        elif errno in self.ERROR_MAP: raise self.ERROR_MAP[errno](errstring, errno, errind, varlist)
        else: raise SNMPError(errstring, errno, errind, varlist)
    
    def __contains__(self, key):
        '''
        Does a get on the target and returns true if there was a value there and false in all other cases (including errors).
        Allows operations like:
            if 'ifDescr.2' in session: ...
        @return: True if the object is in the target's MIB, false otherwise (including SNMP timeouts).
        '''
        try:
            return True if self.get_data(key) else False
        except SNMPError: return False
    
    def __setitem__(self, key, value):
        '''
        Does an snmp set on the target for one or more varbinds.
        Allows operations like:
            session['sysContact.0'] = 'Fred'
            session['ifIndex.1 ifIndex.2 sysLocation.0'] = 2, 1, 'Closet'
        @raise SNMPError: Will raise an SNMPError on any failure -- see documentation for specific exceptions.
        '''
        if not isinstance(value, tuple): value = (value,) #Handle a single value
        #Line up the OID and the values passed in
        self.set_data(*[(oid, val) for oid,val in map(None,key.replace(',',' ').split(),value)] )
        
    def __getitem__(self, key):
        '''
        Does an snmp get on the target for one or more varbinds.
        Allows operations like:
            print session['ifDescr.2 ifOperStatus.2']
            time = session['sysUpTime.0']
        @return: Returns a single value if one OID was given, or a tuple of values if multiple OIDs were given.
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        ''' 
        return self.get_data(*key.replace(',',' ').split())
    
    def get_next_data(self, *args, **kwargs):
        '''
        Perform an SNMP getnext on the provided oids. Example:
            session.get_next_data('sysDescr', 'ifEntry')
        @param oid: A string with either the numerical oid or friendly name.
        @return: Returns a tuple containing the results. If no result was found, None is returned for that oid.
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        '''
        varlist = netsnmp.VarList(*[netsnmp.Varbind(oid) for oid in args])
        result = self.getnext(varlist)
        if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
        return result[0] if len(result) == 1 else result
        
    def get_next_data_oids(self, *args, **kwargs):
        '''
        Perform an SNMP getnext on the provided oids. This returns additional information about what was retrieved. 
        Example:
            session.get_next_data('sysDescr', 'ifEntry')
        @param oid: A string with either the numerical oid or friendly name.
        @return: Returns a list containing tuples with the following format:
            (tag, iid, value, type)
                tag: The name of the object returned, or OID if useNumericOids is true. Does not contain the index or scalar index of the object.
                     For example, in sysDescr.0, this would be the sysDescr part.
                iid: The index or scalar index of the object. For example in sysDescr.0, this would be the 0 part.
                value: The actual value returned. 
                type: The data type of the value. 
            If there was no data, it will return an entry that looks like this: ('ifEntry', '', '', 'NOSUCHOBJECT')
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        '''
        varlist = netsnmp.VarList(*[netsnmp.Varbind(oid) for oid in args])
        self.getnext(varlist) 
        if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
        result = [(varbind.tag, varbind.iid, varbind.val, varbind.type) for varbind in varlist]
        return result[0] if len(result) == 1 else result
    
    def get_data(self, *args, **kwargs):
        '''
        Perform an SNMP getnext on the provided oids. Example:
            session.get_next_data('sysDescr', 'ifEntry')
        @param oid: A string with either the numerical oid or friendly name.
        @return: Returns a tuple containing the results. If no result was found, None is returned for that oid.
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        '''
        varlist = netsnmp.VarList(*[netsnmp.Varbind(oid) for oid in args])
        result = self.get(varlist)
        if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
        return result[0] if len(result) == 1 else result
    
    def get_data_oids(self, *args, **kwargs):
        '''
        Perform an SNMP get on the provided oids. This returns additional information about what was retrieved. 
        Example:
            session.get_next_data('sysDescr', 'ifEntry')
        @param oid: A string with either the numerical oid or friendly name.
        @return: Returns a list containing tuples with the following format:
            (tag, iid, value, type)
                tag: The name of the object returned, or OID if useNumericOids is true. Does not contain the index or scalar index of the object.
                     For example, in sysDescr.0, this would be the sysDescr part.
                iid: The index or scalar index of the object. For example in sysDescr.0, this would be the 0 part.
                value: The actual value returned. 
                type: The data type of the value. 
            If there was no data, it will return an entry that looks like this: ('ifEntry', '', '', 'NOSUCHOBJECT')
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        '''
        varlist = netsnmp.VarList(*[netsnmp.Varbind(oid) for oid in args])
        self.get(varlist)
        if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
        return [(varbind.tag, varbind.iid, varbind.val, varbind.type) for varbind in varlist]
    
    def _is_oid_numeric(self, oid):
        try: 
            oidlist = oid.split('.')
            if not oidlist[1:]: return False #Catch it if there was a single name
            for x in oidlist[1:]: int(x)
        except ValueError: return False
        else: return True
    
    def get_subtree_data_oids(self, oid):
        '''
        Get all the objects under the specified OID. This method retrieves the data using bulkget operations to minimize the impact of latency.
        @warning: This method will turn on UseLongNames for this operation, and the results will reflect that. 
        @warning: If you are using names, and it hits OIDs it cannot translate, it will stop walking there.
        @warning: When walking with numeric OIDs, we cannot properly get the index out of tables! It will consider the last number to be the index.
        @param oid: A single OID, named or numeric.
        @return: Returns a tuple (for one OID) or a list of tuples (for multiple OIDs) with the following format:
            (tag, iid, value, type)
                tag: The full name of the object returned, or number if useNumericOids is true. Does not contain the index or scalar index of the object.
                     For example, in sysDescr.0, this would be the sysDescr part.
                iid: The index or scalar index of the object. For example in sysDescr.0, this would be the 0 part.
                value: The actual value returned. 
                type: The data type of the value. 
            If there was no data, it will return an entry that looks like this: ('ifEntry', '', '', 'NOSUCHOBJECT')
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        '''
        oldUseLongNames = self.UseLongNames
        oldUseNumeric = self.UseNumeric
        self.UseLongNames = 1 #We need long names if we're using named lookups
        
        try:
            #Silly user is using names and put a number in, help them out!
            if not self.UseNumeric and self._is_oid_numeric(oid): self.UseNumeric = 1
            
            #If we're using names, we need a bit of extra logic to get the full root name
            if not self.UseNumeric:
                #@bug: The returns here will cause loss of the original Numeric/LongNames settings
                fullName = self.get_next_data_oids(oid)
                if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd)
                if not fullName: return [] #There are no more OIDs...
                if fullName[0].rfind(oid) == -1: return [] #There wasn't anything under the table
                root = fullName[0][:fullName[0].rfind(oid)+len(oid)]
            else: #Otherwise, just use the full numeric OID
                root = oid

            
            varlist = netsnmp.VarList(netsnmp.Varbind(oid))
            results = []
    
            #1000 is more than you're going to fit in a PDU, just get as many as will fit
            self.getbulk(0, 1000, varlist)
            if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
     
            #First check adds '.' to make sure it is not a similar name on next elem, 2nd checks for leaves
            while varlist[-1].tag.find(root+'.') == 0 or varlist[-1].tag == root:
                #Add all the results to the current list
                results.extend([(varbind.tag, varbind.iid, varbind.val, varbind.type) for varbind in varlist])
                varlist = netsnmp.VarList(varlist[-1]) #The next request only needs the last OID in the returned list
                self.getbulk(0, 1000, varlist) 
                if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
    
            #Start scanning the individual varbinds for the one outside the tree
            #@todo: Should be able to do this in O(logn), don't know if it'll be faster for these sizes
            for varbind in varlist:
                #First check adds '.' to make sure it is not a similar name on next elem, 2nd checks for leaves
                if varbind.tag.find(root+'.') != 0 and varbind.tag != root: break
                results.append((varbind.tag, varbind.iid, varbind.val, varbind.type))
        finally: #In case of errors, make sure we restore the old setting
            self.UseLongNames = oldUseLongNames 
            self.UseNumeric = oldUseNumeric
            
        return results
        
    def get_subtree_data(self, oid):
        '''
        Get all the objects under the specified OID. This method retrieves the data using bulkget operations to minimize the impact of latency.
        @warning: If you are using names, and it hits OIDs it cannot translate, it will stop walking there.
        @param oid: A single OID, named or numeric.
        @return: Returns a list containing each element under the OID in order. Returns None if there was no data.
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        '''
        oldUseLongNames = self.UseLongNames
        oldUseNumeric = self.UseNumeric
        self.UseLongNames = 1 #We need long names if we're using named lookups
        
        try:
            
            #Silly user is using names and put a number in, help them out!
            if not self.UseNumeric and self._is_oid_numeric(oid): self.UseNumeric = 1
            
            #If we're using names, we need a bit of extra logic to get the full root name
            if not self.UseNumeric:
                #@bug: The returns here will cause loss of the original Numeric/LongNames settings
                fullName = self.get_next_data_oids(oid)
                if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd)
                if not fullName: return [] #There are no more OIDs...
                if fullName[0].rfind(oid) == -1: return [] #There wasn't anything under the table
                root = fullName[0][:fullName[0].rfind(oid)+len(oid)]
            else: #Otherwise, just use the full numeric OID
                root = oid
     
            varlist = netsnmp.VarList(netsnmp.Varbind(oid))
            results = []
    
            #1000 is more than you're going to fit in a PDU, just get as many as will fit
            resultBuf = self.getbulk(0, 1000, varlist)
            if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
     
            while varlist[-1].tag.find(root+'.') == 0 or varlist[-1].tag == root:
                #@todo: Faster way to flatten these lists? :(
                results += resultBuf #Add all the results to the current list
                varlist = netsnmp.VarList(varlist[-1]) #The next request only needs the last OID in the returned list
                resultBuf = self.getbulk(0, 1000, varlist) 
                if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd, varlist)
    
            #Start scanning the individual varbinds for the one outside the tree
            #@todo: Should be able to do this in O(logn), don't know if it'll be faster/worth it for these sizes
            for varbind in varlist:
                if varbind.tag.find(root+'.') != 0 and varbind.tag != root: break
                results.append(varbind.val)
        finally: #In case of errors, make sure we restore the old settings
            self.UseLongNames = oldUseLongNames 
            self.UseNumeric = oldUseNumeric
        
        self.UseLongNames = oldUseLongNames 
        self.UseNumeric = oldUseNumeric
        
        return results

    def get_row_data(self, index, *args):
        '''
        Get the data from a table row for the specified index and columns.
        @warning: Requires that the MIBs are loaded and names are in use.
        Example: Return the ifIndex and ifDescr for interface with ifIndex 2, and print the ifDescr:
            row = session.get_row_data('2', 'ifIndex', 'ifDescr')
            print row.ifDescr
        @param index: The index of the row to access.
        @param columns: The 
        '''
        RowData = namedtuple('RowData', list(args), rename=True)
        return RowData(*self.get_data(*[ arg+'.'+index for arg in args ]))
  
    
    def get_table_indicies(self, oid):
        '''
        Get the indicies from a table.
        @warning: Requires that the MIBs are loaded and names are in use.
        @param oid: The OID of the table.
        @return: A list of the indicies (rows) in the table.
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        '''
        oldUseLongNames = self.UseLongNames
        self.UseLongNames = 1
        
        try:
            fullName = self.get_next_data_oids(oid)
        finally:
            self.UseLongNames = oldUseLongNames
            
        if not fullName: return [] #There are no more OIDs...
        if fullName[0].rfind(oid) == -1: return [] #There wasn't anything under the table
        
        #Search for all entries of the first column, and return only the index.
        return [entry[1] for entry in self.get_subtree_data_oids(fullName[0].split('.')[-1])]
        

    def get_table(self, oid):
        '''
        Get the data from a table object and place it into a dictionary of named tuples. 
        Example: For the ifIndex table, you could access the if description of interface with ifIndex 10 using:
            session.get_table('ifTable')['2'].ifDescr
        @warning: This method will only work with the following conditions:
            - Target OID must be a table (no leaf objects)
            - Target OID needs to be a name
            - The MIB for the table must be available to netsnmp
        @param oid: The OID of the table to query.
        @return: Returns a dictionary of named tuples. The key to the dictionary is the table index, and the
                column names are the indicies to the named tuples.
        @raise SNMPError: Raises an SNMPError if there was an error in netsnmp during the request. This includes timeouts.
        @raise KeyError: I'm very sure that this thing will throw keyerrors like there is no tomorrow.
        @todo: Fix KeyError conditions tomorrow.
        '''
        data = self.get_subtree_data_oids(oid) 
        if not data: return []

        resultDict = {}
        
        #Find the number of rows and initialize the indicies.
        firstColName, rowCount, entryCount = data[0][0], 0, len(data)
        for entry in data:
            if firstColName != entry[0]: break
            rowCount += 1
        
        #Get the names of all the columns
        colCount = entryCount/rowCount
        colNames = []
        for col in xrange(colCount):
            #Take the furthest right name in the OID
            colNames.append(data[col*rowCount][0].split('.')[-1])
        #Create a new type with names for each column
        TableRow = namedtuple('TableRow', colNames, rename=True)
        
        #Load the row data into the dicitonary
        for row in xrange(rowCount):
            rowData = []
            for col in xrange(colCount):
                rowData.append(data[(col*rowCount)+row][2])
            resultDict[data[row][1]] = TableRow(*rowData)
            
        return resultDict
            
    
    def set_data(self, *args):
        '''
        Set one or more OIDs.
        @warning: Requires that the MIBs are loaded.
        Example: Set the sysContact and sysLocation:
            session.set_data( ('sysContact.0','Carl'), ('sysLocation.0','Ottawa') )
        There is also a shorthand:
            session['sysContact.0 sysLocation.0'] = 'Carl','Ottawa'
        @param pair: One or more tuple pairs of (oid, value) to set.
        @return: Returns the varlist after the set.
        @raise SNMPError: Will raise an SNMPError on any failure -- see documentation for specific exceptions.
        '''
        for arg in args: #This is messy, but we need some way of verifying all this, or netsnmp goes all nusty fagan
            if not isinstance(arg, tuple) or len(arg) != 2 or arg[0] == None or arg[1] == None: raise SNMPError('Invalid Set Tuple', 2, 2)
        varlist = netsnmp.VarList(*[netsnmp.Varbind(tag=arg[0], val=arg[1]) for arg in args])
        self.set(varlist)
        if self.ErrorStr: self.raise_error(self.ErrorStr, self.ErrorNum, self.ErrorInd)
        return varlist
    
   


    
    