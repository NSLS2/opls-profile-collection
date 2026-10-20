#import ast, os
#
#def scan_read(name,start_ascii,end,scan_dir):
#    if start_ascii == "all":
#        start=99
#    else:
#        start=start_ascii
#    if scan_dir=="global":
#        print("global directory")
#        directory='/home/xf12id1/.ipython/profile_collection/startup/scans/'
#    else:
#        directory='/home/xf12id1/.ipython/profile_collection/startup/users/ocko/scans/'
#    with open(directory+name, "r") as f:
#            text = f.read()
## Remove the variable assignment
#    dict_text = text.split("=", 1)[1].strip()
#    scan_dict1 ={}
#    file_input = ast.literal_eval(dict_text)
#    names=list(file_input)
#    names_list = [name + "_list" for name in names]
#    loop_list= list(range(len(names_list)))
#    for i in loop_list:
#        s =file_input[names[i]]
#        s = s.strip("[]")
#        elements = [x.strip() for x in s.split(",")]
#    #    print("elements=",elements)
#        if len(elements) ==1:
#            scan_dict1[names_list[i]]=elements[0]
#    # if start >= 99, it does all scans
#        if start == 99:
#            values = list(map(float, elements))
#            scan_dict1[names_list[i]]=values
#            print(elements)
#
#        else:
#            values = list(map(float, elements))
#            print(elements)
#            scan_dict1[names_list[i]]=values[start:end+1]
#    return(scan_dict1)
#        
#
#
#def xr_scan_file(sample_name,scan_name,start,end,scan_dir): 
#    print("in xr_scan_file:",scan_name,start,end,scan_dir)
#    tmp=scan_read(scan_name,start,end,scan_dir)  
#    alpha_start_list=tmp["alpha_start_list"]
#    alpha_stop_list=tmp["alpha_stop_list"]
#    tmp_np=tmp["number_points_list"]
#    number_points_list=[int(x) for x in tmp_np]
#    tmp_att =tmp["auto_atten_list"]
#    auto_atten_list=[int(x) for x in tmp_att]
#    exp_time_list =tmp["exp_time_list"]
#    s2_vg_list=tmp["s2_vg_list"]
#    precount_time_list=tmp["precount_time_list"]
#    wait_time_list=tmp["wait_time_list"]
#    x2_offset_start_list=tmp["x2_offset_start_list"]
#    x2_offset_stop_list=tmp["x2_offset_stop_list"]
#    block_offset_list=tmp["block_offset_list"]
#
#    print("\nstart",alpha_start_list)
#    print(alpha_stop_list)
#    print(number_points_list)
#    print(auto_atten_list)
#    print(exp_time_list)
#    print(s2_vg_list)
#    print("precount",precount_time_list)
#    print("wait_time",wait_time_list)
#    print("x2_offset_start",x2_offset_start_list)
#    print("x2_offset_stop",x2_offset_stop_list)
#    print("block_offset",block_offset_list)
#
#
#    scan_p={"start":alpha_start_list,
#        "stop":alpha_stop_list,
#        "n":number_points_list,
#        "atten":auto_atten_list,
#        "s2vg":s2_vg_list,
#        "exp_time":exp_time_list,
#        "pre_time":precount_time_list,
#        "wait_time":wait_time_list,
#        "x2_offset_start":x2_offset_start_list,
#        "x2_offset_stop":x2_offset_stop_list,
#        "beam_block_offset":block_offset_list}
#        
#    yield from bps.mv(geo.det_mode,1)
#    yield from reflection_scan_full(scan_param=scan_p,
#        md={'sample_name': sample_name},
#        detector=lambda_det, 
#        tilt_stage=False)
#
#
##xr_scan_file("scan_xr2.txt",99,3)
#
## not sure why the message below is generated
##  xr_scan_file("scan_xr2.txt",99,3,dir="local")
##Out[86]: <generator object xr_scan_file at 0x7f4687ffccc0>
#
## Seems like I may have to run RE as xr_scan_file calls motors and the detector.
#
#
#        
#
#        
#
#
