ENTRY = load '/etc/passwd' using PigStorage(':');  -- load the passwd file
IDS = foreach ENTRY generate $0 as id;  -- extract the user IDs

store IDS into './ids.out';  -- write the results to a file name ids.out
