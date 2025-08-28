USE ROLE ACCOUNTADMIN ; 

USE SCHEMA IK_DEV.AUTOMATION ; 



// set up secret -> credentials have been redacted for security reasons

CREATE or replace SECRET ik_dev.automation.bc_integration_credentials
    TYPE = password
    USERNAME ='e6bb21ac-41d6-48fc-bdf8-e0aeb1316b24'
    PASSWORD='zEB8Q~ZPyUiRe7PS7u1GcM~SG_KNcJKYVN.VabIb' ;



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


