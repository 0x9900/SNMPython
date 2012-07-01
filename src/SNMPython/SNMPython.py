'''
Created on Jun 30, 2012

@author: cverge
'''

import netsnmp
from collections import namedtuple


class SNMPError(Exception):
    
    def __init__(self, errstring, errno=None, errind=None, varlist=None):
        self.errstring = errstring
        self.errno = errno
        self.errind = errind
        self.varlist = varlist
        
    def __str__(self):
        error = ["%s " % self.errstring]
        if self.errno != None: error.append("  System Error Number: %d" % self.errno)
        if self.errind != None: error.append("  SNMP Error Number: %d" % self.errind)
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
    classdocs
    '''


    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        netsnmp.Session.__init__(self, *args, **kwargs)
    
    #Copied wholesale from Microsoft's site of all things
    ERROR_MAP = {
                1: SNMPTooBigError, #The agent could not place the results of the requested SNMP operation in a single SNMP message.
                2: SNMPNoSuchNameError, #The requested SNMP operation identified an unknown variable.
                3: SNMPBadValueError, #The requested SNMP operation tried to change a variable but it specified either a syntax or value error.
                4: SNMPReadOnlyError, #The requested SNMP operation tried to change a variable that was not allowed to change, according to the community profile of the variable.
                5: SNMPGenErr, #An error other than one of those listed here occurred during the requested SNMP operation.
                6: SNMPNoAccessError, #The specified SNMP variable is not accessible.
                7: SNMPWrongTypeError, #The value specifies a type that is inconsistent with the type required for the variable.
                8: SNMPWrongLengthError,
                9: SNMPWrongEncodingError,
               10: SNMPWrongValueError,
               11: SNMPNoCreationError,
               12: SNMPInconsistentValueError,
               13: SNMPResourceUnavailableError,
               14: SNMPCommitFailedError,
               15: SNMPUndoFailedError,
               16: SNMPAuthorizationError,
               17: SNMPNotWritableError,
               18: SNMPInconsistentNameError            
               }
    
    def raise_error(self, errstring, errno, errind, varlist):
        if errind == -24: raise SNMPTimeoutError(errstring, errno, errind, varlist)
        elif errno in self.ERROR_MAP: raise self.ERROR_MAP[errind](errstring, errno, errind, varlist)
        else: raise SNMPError(errstring, errno, errind, varlist)
    
    def __contains__(self, key):
        try:
            return True if self.get_data(key) else False
        except SNMPError: return False
    
    
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
        if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
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
        if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
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
        if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
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
                fullName = self.get_next_data_oids(oid)
                if not fullName: return [] #There are no more OIDs...
                if fullName[0].rfind(oid) == -1: return [] #There wasn't anything under the table
                root = fullName[0][:fullName[0].rfind(oid)+len(oid)]
            else: #Otherwise, just use the full numeric OID
                root = oid

            
            varlist = netsnmp.VarList(netsnmp.Varbind(oid))
            results = []
    
            #1000 is more than you're going to fit in a PDU, just get as many as will fit
            self.getbulk(0, 1000, varlist)
            if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
     
            #First check adds '.' to make sure it is not a similar name on next elem, 2nd checks for leaves
            while varlist[-1].tag.find(root+'.') == 0 or varlist[-1].tag == root:
                #Add all the results to the current list
                results.extend([(varbind.tag, varbind.iid, varbind.val, varbind.type) for varbind in varlist])
                varlist = netsnmp.VarList(varlist[-1]) #The next request only needs the last OID in the returned list
                self.getbulk(0, 1000, varlist) 
                if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
    
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
                fullName = self.get_next_data_oids(oid)
                if not fullName: return [] #There are no more OIDs...
                if fullName[0].rfind(oid) == -1: return [] #There wasn't anything under the table
                root = fullName[0][:fullName[0].rfind(oid)+len(oid)]

            else: #Otherwise, just use the full numeric OID
                root = oid
    
            
            varlist = netsnmp.VarList(netsnmp.Varbind(oid))
            results = []
    
            #1000 is more than you're going to fit in a PDU, just get as many as will fit
            resultBuf = self.getbulk(0, 1000, varlist)
            if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
     
            while varlist[-1].tag.find(root+'.') == 0 or varlist[-1].tag == root:
                #@todo: Faster way to flatten these lists? :(
                results += resultBuf #Add all the results to the current list
                varlist = netsnmp.VarList(varlist[-1]) #The next request only needs the last OID in the returned list
                resultBuf = self.getbulk(0, 1000, varlist) 
                if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
    
            #Start scanning the individual varbinds for the one outside the tree
            #@todo: Should be able to do this in O(logn), don't know if it'll be faster/worth it for these sizes
            for varbind in varlist:
                if varbind.tag.find(root+'.') != 0 and varbind.tag != root: break
                results.append(varbind.val)
        finally: #In case of errors, make sure we restore the old setting
            self.UseLongNames = oldUseLongNames 
            self.UseNumeric = oldUseNumeric
            
        return results

    def get_row_data(self, index, *args):
        RowData = namedtuple('RowData', list(args), rename=True)
        return RowData(*self.get_data(*[ arg+'.'+index for arg in args ]))
  
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
        print colNames
        TableRow = namedtuple('TableRow', colNames, rename=True)
        
        #Load the row data into the dicitonary
        for row in xrange(rowCount):
            rowData = []
            for col in xrange(colCount):
                rowData.append(data[(col*rowCount)+row][2])
            resultDict[data[row][1]] = TableRow(*rowData)
            
        return resultDict
            
    
    def set_data(self, *args):
        for arg in args: #This is messy, but we need some way of verifying all this, or netsnmp goes all nusty fagan
            if not isinstance(arg, tuple) or len(arg) != 2 or arg[0] == None or arg[1] == None: raise SNMPError('Invalid Set Tuple', 2, 2)
        result = self.set(netsnmp.VarList(*[netsnmp.Varbind(tag=arg[0], val=arg[1]) for arg in args]))
        if self.ErrorStr: raise SNMPError(self.ErrorStr, self.ErrorNum, self.ErrorInd)
        return result
    
    def __setitem__(self, key, value):
        if not isinstance(value, tuple): value = (value,) #Handle a single value
        print [(oid, val) for oid,val in map(None,key.replace(',',' ').split(),value)] 
        self.set_data(*[(oid, val) for oid,val in map(None,key.replace(',',' ').split(),value)] )
        
    
    def __getitem__(self, key):
        return self.get_data(*key.replace(',',' ').split())
    
   
    
if __name__ == '__main__':
    
    session = SNMPythonSession(DestHost='23.11.0.11', Community='private', Version=2)
    session.UseNumeric = 0
    failedTabs = []
#    for table in open('tabList', 'r'):
#        try:
#            print "Trying ", table
#            session.get_table(table.split('(')[0])
#        except:
#            failedTabs.append(table)
#    
    try:
        session['sysContact.0 ifDescr.1']
    except SNMPError, e:
        print e
        print e.varlist 
    
    
#    bind = netsnmp.Varbind('ifDescr.1', val='notcarl')
#    print session.set_data( ('sysContact.0','someone') , ('ifAdminStatus.1', 1) )
#    print session['sysContact.0 ifAdminStatus.1']
#    session['sysContact.0', 'sysLocation.0'] = 'carl', 'notcarl'
#    
    
    
    
    
    
    #print len(failedTabs), failedTabs
    #print session.get_table('ifTable')
    #for entry in session.get_subtree_data_oids('.1.3.6.1.2.1.2.2'): print entry
    #print session.get_row_data('35684352','ifDescasdsar','ifMtu','ifType')
    #print session.get_table('vRtrAdvPrefixTable')
#   # print session.get_table('vRtrMplsLspTable')
#    print session.get_table('vRtrIfTable')['1.4'].vRtrIfOperState
#    print session.get_next_data('sysUpTime', 'sysName')
    
    