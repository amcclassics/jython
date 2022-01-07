envVarName="ORACLE_JDBC_DRIVER_PATH"
envVarValue="/opt/IBM/WebSphere/jdbc/ojdbc6.jar"
cellName=AdminControl.getCell()
nodes = AdminNodeManagement.listNodes()

print "Removing the variable "+envVarName+" at Cell scope in case it already exist"
#AdminTask.removeVariable(['-variableName '+envVarName+' -scope Cell='+cellName])

print "Setting the variable "+envVarName+" to "+envVarValue+" at Cell scope"
#AdminTask.setVariable(['-variableName '+envVarName+' -variableValue '+envVarValue+' -scope Cell='+cellName])

print "Getting list of Nodes in the Cell ..."
for eachNode in nodes:
   myNode,somedata = eachNode.split('(')
   print "Removing the variable "+envVarName+" at Node "+myNode+" scope in case it already exist"
   AdminTask.removeVariable(['-variableName '+envVarName+' -scope Cell='+cellName+':Node='+myNode])

   print "Setting the variable "+envVarName+" at Node "+myNode+" scope "
   AdminTask.setVariable(['-variableName '+envVarName+' -variableValue '+envVarValue+' -scope Cell='+cellName+':Node='+myNode])
#endFor

print "Saving changes.."
AdminConfig.save()
