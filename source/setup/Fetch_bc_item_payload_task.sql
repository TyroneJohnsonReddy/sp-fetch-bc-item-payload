// task has already been set up, below is for reference

USE ROLE SYSADMIN ; 

create or replace task IK_DEV.AUTOMATION.FETCH_BC_ITEM_PAYLOAD_TASK
	warehouse=COMPUTE_WH
	schedule='USING CRON 0 6 * * * Africa/Johannesburg'
	as call ik_dev.automation.fetch_bc_item_payload() ; 