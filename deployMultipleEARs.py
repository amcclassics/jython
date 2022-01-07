import java.lang.String as String  # To use indexOf() later
import java.util as util
import java.io as javaio
import platform
import time,sys
line = java.lang.System.getProperty("line.separator")


appList=[]
try:
   appToDeploy = sys.argv[0]
   appList.append(appToDeploy)
except:
   print "\nDid not receive app as argument, using list..."
   appList.append("AppEar1")
   appList.append("AppEar2")
   appList.append("ApplicationWebEAR1")
   appList.append("ApplicationWebEAR2")
   print appList
#endTry


################################
## Setup appserver variables and determine AdminApp scope
################################

appDir = "/opt/IBM/WebSphere/artifacts"

scopeType = "Server"

####  Only set scopeName if scopeType=ServerCluster, otherwise we will look for appserver1
## scopeType = "ServerCluster"
## scopeName = 

#Set appserver and node name based on "appserver1"
if scopeType == "Server":
   print "\nLooking for appserver1..."
   appServId=AdminConfig.list("Server", "appserver1.*")

   try:
      appServName=AdminConfig.showAttribute(appServId, 'name')
      appServObj=AdminControl.queryNames('WebSphere:name='+appServName+',type=Server,*')
   except:
      print "Could not find appserver1, an error has occurred.\nScript will exit"
      exit()
   #endTry

   for eachProperty in appServObj.split(","):
      thisPropName,thisPropVal = eachProperty.split("=")
      if thisPropName == "node":
         nodeName = thisPropVal
   #endFor

   scopeName = appServName
   appScopeTarget = "-node "+nodeName+" -server "+scopeName

elif scopeType == "ServerCluster":
   appScopeTarget = "-cluster "+scopeName
#endIf

print "Deploying apps to scope: "+appScopeTarget

################################
#### Loop through app list and deploy / install / update
################################

print "Processing deploy list "+str(appList)+" ..."

for appName in appList:

################################
## Deploy the EAR to server or cluster
################################

   appPath = appDir+"/"+appName+".ear"
   appExists = AdminApplication.checkIfAppExists(appName)

   ## If application already exists, perform update
   if appExists == 'true':
      appTarget = AdminApplication.getAppDeploymentTarget(appName)

      for node in appTarget:
         s = String(node)
         temp = s.indexOf(scopeName)
         if temp == 0:
            print appName + " already exists at " + str(appTarget)  + ".\nUpdating with " + appPath +"\n"
            appArgs = ["-operation", "update", "-contents", appPath, "-usedefaultbindings"]
            print "Updating app with options: "+str(appArgs)+"\n"
            AdminApp.update(appName,'app',appArgs)

   ## If application doesn't exist, install it now.
   else:
      print "App "+appName+" was not found. Installing it now...\n"

      ## Build the application arguments

      appArgs = [ appScopeTarget, 
       "-appname "+appName,
       "-usedefaultbindings",
       "-useMetaDataFromBinary",
       "-usedefaultbindings",
       "-useMetaDataFromBinary",
       "-defaultbinding.virtual.host", "default_host"]

      print "Installing app with options: "+str(appArgs)+"\n"
      AdminApp.install(appPath, appArgs)
   #end if


   ###############################################
   ## Save changes 
   ###############################################
   print "\nSaving changes...\n"
   AdminConfig.save()

   ###############################################
   ## Sync nodes; If cluster
   ###############################################
   if scopeType == "ServerCluster":
      print "\nSyncing the nodes...\n"
      AdminNodeManagement.syncActiveNodes()
   #endif

#endFor
