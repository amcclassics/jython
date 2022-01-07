# Create the list as AppServerName,JvmCustomPropName,JvmCustomPropValue
# For example: WebSphere_Portal,ENV_NAME,STAGE
customPropList = []
jvmName="appserver1"
customPropList.append(jvmName+",ENVID,TEST")
customPropList.append(jvmName+",SERVERID,1A")

for customProp in customPropList:
   serverName,jvmPropName,jvmPropVal = customProp.split(",")
   print "Setting JVM Custom Property "+jvmPropName+" to value "+jvmPropVal+" on appserver "+serverName
   adminTaskArgs = '[-serverName '+serverName+' -propertyName '+jvmPropName+' -propertyValue '+jvmPropVal+']'
   try:
      AdminTask.setJVMSystemProperties(adminTaskArgs)
   except:
      print "Could not create JVM Custom Property. An error has occurred..."
   #endTry
#endFor
AdminConfig.save()
