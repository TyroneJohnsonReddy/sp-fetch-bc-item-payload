// network rules and external access integration has been set up, below is for reference

USE ROLE ACCOUNTADMIN ; 

USE SCHEMA IK_DEV.AUTOMATION ; 



// set up secret -> credentials have been redacted for security reasons

CREATE or replace SECRET ik_dev.automation.bc_integration_credentials
    TYPE = password
    USERNAME ='[REDACTED]'
    PASSWORD='[REDACTED]' ;



// set up network rules 

CREATE OR REPLACE NETWORK RULE ik_dev.automation.microsoft_login_network_rule
  TYPE = HOST_PORT
  VALUE_LIST = ('login.microsoftonline.com:443') 
  MODE= EGRESS ;


  CREATE OR REPLACE NETWORK RULE ik_dev.automation.business_central_network_rule
  TYPE = HOST_PORT
  VALUE_LIST = ('api.businesscentral.dynamics.com') 
  MODE= EGRESS ;

  CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION bc_access_integration
  ALLOWED_NETWORK_RULES = (microsoft_login_network_rule,business_central_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (ik_dev.automation.bc_integration_credentials)
  ENABLED = true ;


grant usage on integration bc_access_integration to role 
SYSADMIN ; 

