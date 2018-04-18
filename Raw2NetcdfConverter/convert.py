'''
Description: 
This Modul convert the .raw files to .nc files. 
In future, the function should be abe to store several pings within one file


    
Author: 
Dr. Sindre Vatnehol (PhD)
Institute of Marine Research, Norway

Mail: 
sindre.vatnehol@imr.no

Tlf.: 
+47 900 79 376


Project: 
REDUS (Reducing uncertainty in stock assessment)  
www.redus.no
'''


    
import glob,os, pynmea2,os.path
from netCDF4 import Dataset
import numpy as np
from shutil import copyfile
from .ReadRawData import ReadRawData
from .template import addAnnotation, addEnvironment, addPlatform, addProvenance
from .template import addGlobalAttributes, writePlatformData, createSonarData
from .template import addVendorSpecificGrp, addSonarData, addEnvironmentData
import os

    



def getGPSsourcesfromdata(NMEA_info): 
    
    PriorityList = np.array(('RMC', 'GLL','GGA'))
    
    Tempo = []
    for LoopIndex0 in range(len(NMEA_info)): 
        info = NMEA_info[LoopIndex0]
        try: 
            msg = pynmea2.parse(info,check= False)
            try: 
                msg.longitude
                Tempo = np.hstack((Tempo,info.split(',')[0][-3:]))
            except AttributeError: 
                k=1
        except pynmea2.nmea.ParseError:
            k=1
            
             
    return [i for i, j in zip(PriorityList, np.unique(Tempo)) if i == j]
               
    
    
    
def WelcomeScreen(projectName): 
    print(projectName)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('    >=>      /\      >=>          >=>           ')
    print('  >=>       /  \           >=>         >=>      ')
    print('           / >=>\                               ')
    print('   >=>    /      \                 >=>          ')
    print('         /   >=>  \      >=>                >=> ')
    print('        / >=>      \              >=>    >=>    ')
    print('_______/________>=>_\___________________________')
    print('')

    
    
    
def Raw2NetcdfConverter(directoryToRaw,vessel_name,platform_type,
                        platform_code,maxPingInFile,MaxNumberOfFilesInNC,
                        directory): 
    '''
    Description: 
        Protocol to convert sonar raw data to netcdf
    '''
    
    
    
    
    #Clear terminal window
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
    
    
    #print welcome screen
    WelcomeScreen('convertrawtonetcdf')
    
    
    
    #Get the location of the templet
    this_dir, this_filename = os.path.split(__file__)
    template_file = os.path.join(this_dir, "data", "source_template.nc")
    

    
    #Check if netcdf folder exist
    #If not create the directory
    if (not os.path.isdir(directory)): 
        os.makedirs(directory)
        
    

    #Change the directory to the raw files
    os.chdir(directoryToRaw)
    
    
    
    #Go through each .raw file in folder
    for filename in sorted(glob.glob("*.raw")):
        
        
        #Display msg to user
        print('Converting '+filename+' to netcdf')
        
        
        
        #Change the directory back to .raw folder. 
        #Later it will be send to the netcdf folder
        os.chdir(directoryToRaw)
        
        
            
        #open .raw file
        fid = open(filename,mode='rb')
        
       
        
        #Read the .raw file according to SIMRAD spesifications
        FileData = ReadRawData(fid,12)
        
        
        
        #Get the transduser rotation
        #This is a correction of the true direction of the beams
        transducer_rotation =  FileData.dirz
                    
        
        #Set the directory to where the netcdf should be stored
        os.chdir(directory)
        
            
        #Set the name of the .nc file to the same as the first .raw file                        
        ncfilename=filename[:-4]+'.nc'
    

        #Copy template to current folder, and rename it
#        copyfile(template_file,ncfilename)

        
        #open new .nc file
        f =Dataset(template_file,'r') 
        fid = Dataset(ncfilename,'w')

        #Add global attribtues
        addGlobalAttributes(fid,filename)
        
        #Create annotation level
        addAnnotation(fid)
        
        #create environment level
        addEnvironment(fid)
        
        #create platform level
        addPlatform(fid,platform_code, vessel_name, platform_type,f)
        
        #create the provinence group
        addProvenance(fid)
        
        #create sonar data group
        createSonarData(fid)

        #create Vendor specific group
        addVendorSpecificGrp(fid)

        #Get the list of nmea sources according to priority list
        GPSsourceList = getGPSsourcesfromdata(FileData.NMEA_info)
        
        #Write platform data 
        writePlatformData(FileData,GPSsourceList,fid)
        
        #Write environment data
        addEnvironmentData(FileData, fid)

        #Write sonar data        
        addSonarData(FileData,fid,transducer_rotation)
                        
        fid.close()

            
            
   #'''OLD'''         
            
            
            
            
            
            
                        
                        
                            
        #Set the time of creation to the .nc file
#        filetime=pytz.timezone('Europe/Oslo').localize(datetime.datetime.utcnow())
        
        
        #Write creation of file
#        f.date_created = str(filetime).replace(' ','T')
#        f.keywords = 'Simrad '+filename[:4]
#        f.sonar_convention_authority  = 'ICES'
#        f.sonar_convention_version  = '1.0'
#        f.summary = 'Converted files from .raw format'
#        f.title = 'raw to nc converted files'

        
        
        #Add .raw file name to list in Provenance
        #Add this so it is more easier to see which files that is included
#        addvar = f.groups['Provenance'].variables['source_filenames']
#        addvar[NumberOfFilesInNC-1] = filename

     

        #Write Provenance information about the new file
#        f.groups['Provenance'].conversion_software_name= ConversionSoftwareName 
#        f.groups['Provenance'].conversion_software_version= ConversionSoftwareVersion
#        f.groups['Provenance'].conversion_time= str(filetime)
#        
#        
#        addvar = fid.groups['Provenance'].variables['source_filenames']
#        addvar[NumberOfFilesInNC-1] = filename

        
        
        #Add information of the sonar
#        f.groups['Sonar'].sonar_model = str(FileData.soundername)
#        f.groups['Sonar'].sonar_software_version = str(FileData.version)
#        f.groups['Sonar'].sonar_serial_number = 'NaN'
#        

        #Add information of the platform
#        f.groups['Platform'].platform_code_ICES = platform_code 
#        f.groups['Platform'].platform_name = vessel_name
#        f.groups['Platform'].platform_type = platform_type
#        
#
#        f.groups['Sonar'].createGroup('Beam_group2')
#        f.groups['Sonar'].groups['Beam_group2'].beam_mode = 'Horizontal'
#        f.groups['Sonar'].groups['Beam_group2'].conversion_equation_type = 'type_1'
#        f.groups['Sonar'].groups['Beam_group1'].beam_mode = 'Vertical'
#        f.groups['Sonar'].groups['Beam_group1'].conversion_equation_type = 'type_1'
#    
#
#        #copy beam group and add information
#        addvar = f.groups['Sonar'].groups['Beam_group1']
#        dsout = f.groups['Sonar'].groups['Beam_group2']
    
#
#        for name, dimension in addvar.dimensions.items():
#            dsout.createDimension(name, (len(dimension) if not dimension.isunlimited() else None))
#
#            
#            
#        for name, variable in addvar.variables.items():
#            dsout.createVariable(name, variable.datatype, variable.dimensions)
#            dsout[name][:] = addvar[name][:]
#
#
#            # copy variable attributes all at once via dictionary
#            dsout[name].setncatts(addvar[name].__dict__)
#            if name == 'beam': 
#                for i in range(len(addvar.dimensions['beam'])): 
#                    addvar['beam'][i] = str(i+1)
#                    dsout['beam'][i] = str(i+1)
            
            
#        f.groups['Platform'].createDimension('time3',None)
#        f.groups['Platform'].createVariable('time3',np.int64,'time3')
#        f.groups['Platform'].variables['time3'].setncatts(f.groups['Platform'].variables['timeN'].__dict__)
##
#
#
#        f.groups['Sonar'].groups['Beam_group2'].variables['non_quantitative_processing'].flag_values = '0, 1, 2, 3'
#        f.groups['Sonar'].groups['Beam_group1'].variables['non_quantitative_processing'].flag_values = '0, 1, 2, 3'
#        f.groups['Sonar'].groups['Beam_group2'].variables['non_quantitative_processing'].flag_meanings = "no_non_quantitative_processing simrad_weak_noise_filter simrad_medium_noise_filter simrad_strong_noise_filter"
#        f.groups['Sonar'].groups['Beam_group1'].variables['non_quantitative_processing'].flag_meanings = "no_non_quantitative_processing simrad_weak_noise_filter simrad_medium_noise_filter simrad_strong_noise_filter"





      
#        #Run through each NMEA information 
#        for LoopIndex0 in range(len(FileData.NMEA_time)): 
#            
#            
#            #Load  NMEA time and info
#            Time = FileData.NMEA_time[LoopIndex0]
#            info = FileData.NMEA_info[LoopIndex0]
#
#
#            #A bug fix
#            if Time[0]>0: 
#                if LoopIndex0==0: 
#                    
#                    #Add some information of the annotation, may be deleted later                    
#                    addvar = f.groups['Annotation'].variables['time']
#                    addvar[annotation_index] = Time[0]*100
#
#                    addvar = f.groups['Annotation'].variables['annotation_category']
#                    addvar[annotation_index] = 'Update'
#                    
#                    addvar = f.groups['Annotation'].variables['annotation_text']
#                    addvar[annotation_index] = 'Converted '+filename+' to' +ncfilename
#
#             
#                    addvar = fid.groups['Annotation'].variables['time']
#                    addvar[annotation_index] = Time[0]*100
#
#                    addvar = fid.groups['Annotation'].variables['annotation_category']
#                    addvar[annotation_index] = 'Update'
#                    
#                    addvar = fid.groups['Annotation'].variables['annotation_text']
#                    addvar[annotation_index] = 'Converted '+filename+' to' +ncfilename
#
#
#                    annotation_index = annotation_index+1
#                    
#                    
#                    
#                #Open Platform group                
#                addvardir = f.groups['Platform'].groups['NMEA']
#                addvar = addvardir.variables['time']                            
#                addvar[LoopIndex3]=  Time[0]*100
#                addvar = addvardir.variables['NMEA_datagram']                            
#                addvar[LoopIndex3]=  info

#
#                LoopIndex3=LoopIndex3+1
#                
#                
#                #Get the preffered telegram, 'H
#                if info.split(',')[0][-3:]==WhereNMEA[-3:]: 
#                    
#                    msg = pynmea2.parse(info,check= False)
#                    
#                    
#                    #Check if nmea telegram is corrupted
#                    
#                    
#                    try:
#                        msg.latitude
#                        
#                        #Parse the msg
#                        
#                        if (Time[0]-old_time)>0: 
                        
                            #Add NMEA information to platform
#                            addvar = f.groups['Platform'].variables['latitude']                            
#                            addvar[LoopIndex1]=  msg.latitude
#                            
#                            addvar = f.groups['Platform'].variables['longitude']                            
#                            addvar[LoopIndex1]=  msg.longitude
#                            
#                            addvar = f.groups['Platform'].variables['time1']                            
#                            addvar[LoopIndex1]=  Time[0]*100


#                            addvar = fid.groups['Platform'].variables['latitude']                            
#                            addvar[LoopIndex1]=  msg.latitude
#                            
#                            addvar = fid.groups['Platform'].variables['longitude']                            
#                            addvar[LoopIndex1]=  msg.longitude
#                            
#                            addvar = fid.groups['Platform'].variables['time1']                            
#                            addvar[LoopIndex1]=  Time[0]*100
#    
#    
#                            old_time = Time[0]
#                            
#                            
#                            LoopIndex1 = LoopIndex1+1 
#                        else: 
#                            print('         *NMEA was replicated',end='\r')
#                            
#                    except AttributeError:
#                        print('         *Bad GPS',end='\r')
#                        
                        
                        
                        
                #Get the information of vessel heading from the preferred nmea telegram                     
#                elif info.split(',')[0][-3:]==WhereNMEAheading[-3:]:
#                    
#                    'ok'
#                    #Parse information to get heading information
#                    msg = pynmea2.parse(info)
#                    
#                    
#                    #Write information
#                    addvar = f.groups['Platform'].variables['heading']                            
#                    addvar[LoopIndex2]=  msg.heading
#                    addvar = f.groups['Platform'].variables['time2']                            
#                    addvar[LoopIndex2]=  Time[0]*100
#                    LoopIndex2=LoopIndex2+1
                    
                    
        
        #Set nan to unused values
#        f.groups['Platform'].variables['speed_ground'][0] = np.nan
        
        
        
#        #Loop through every ping in raw fil
#        for LoopIndex0 in range(0,len(FileData.PingData)): 
#            
#            
#            #If there is information inside the ping continue
#            if not FileData.NMEA[LoopIndex0] ==[]:
#                
#                
#                #Get the time of the ping from nmea
#                Time = FileData.NMEA[LoopIndex0]
#                
#
#                #Get relevant information from raw data
#                sampleinterval = FileData.PingData[LoopIndex0].sampleinterval[0]
#
#                frequency = FileData.PingData[LoopIndex0].frequency[0]                  
#
#                transmitpower = FileData.PingData[LoopIndex0].transmitpower[0]       
#
#                pulslength = FileData.PingData[LoopIndex0].pulslength[0]     
#
#                bandwidth = FileData.PingData[LoopIndex0].bandwidth[0] 
#
##                heave = FileData.PingData[LoopIndex0].heave[0]
#
##                roll = FileData.PingData[LoopIndex0].roll[0]
##
##                pitch = FileData.PingData[LoopIndex0].pitch[0]
##        
#                transducer_gain = FileData.PingData[LoopIndex0].gainrx+FileData.PingData[LoopIndex0].gaintx
#                
#                transmitmode = FileData.PingData[LoopIndex0].transmitmode[0]
#
#                dirx = FileData.PingData[LoopIndex0].dirx
#
#                diry = FileData.PingData[LoopIndex0].diry
#
#                equivalentbeamangle = FileData.PingData[LoopIndex0].equivalentbeamangle
#
#                BeamAmplitudeData =  FileData.PingData[LoopIndex0].BeamAmplitudeData
#                
#                BeamAmplitudeData_imaginary =  FileData.PingData[LoopIndex0].BeamAmplitudeData_imaginary
#
#                absorption = FileData.PingData[LoopIndex0].absorptioncoefficient[0]
#
#                soundvelocity = FileData.PingData[LoopIndex0].soundvelocity[0]
#
#                BWalong = FileData.PingData[LoopIndex0].beamwidthalongshiprx
#                
#                BWatwh=FileData.PingData[LoopIndex0].beamwidthathwartshiprx
#
#                BWalongTX = FileData.PingData[LoopIndex0].beamwidthhorizontaltx[0]
#
#                BWatwhTX=FileData.PingData[LoopIndex0].beamwidthverticaltx[0]
#
#                NoiseFilter=FileData.PingData[LoopIndex0].noisefilter[0]
#
#               
#                #Convert beam direction into unit vectors
#                dirx_u = np.cos((dirx)*np.pi/180)*np.cos((diry+transducer_rotation[0])*np.pi/180)
#                
#                diry_u = np.cos((dirx)*np.pi/180)*np.sin((diry+transducer_rotation[0])*np.pi/180)
#                
#                dirz_u = np.sin((dirx)*np.pi/180)
#                
#                
#
#                #Get all unique frequencies and store it
#                if not frequency in Frequency_index: 
##
#                    Frequency_index = np.hstack((Frequency_index,frequency))
##                    
##                    
##                    #Write Environment information
##                    f.groups['Environment'].variables['frequency'][len(Frequency_index)-1]=frequency
##                    f.groups['Environment'].variables['absorption_indicative'][len(Frequency_index)-1]=absorption
##                    f.groups['Environment'].variables['sound_speed_indicative'][len(Frequency_index)-1]=soundvelocity
##
##                    #Write Environment information
#                    fid.groups['Environment'].variables['frequency'][len(Frequency_index)-1]=frequency
#                    fid.groups['Environment'].variables['absorption_indicative'][len(Frequency_index)-1]=absorption
#                    fid.groups['Environment'].variables['sound_speed_indicative'][len(Frequency_index)-1]=soundvelocity
#
#
#                #Write platform data to group
##                addvar = f.groups['Platform'].variables['vertical_offset']                            
##                addvar[LoopIndex0]=  heave
##                
##                addvar = f.groups['Platform'].variables['roll']                            
##                addvar[LoopIndex0]=  roll
##                
##                addvar = f.groups['Platform'].variables['pitch']                            
##                addvar[LoopIndex0]=  pitch
##                
##
##                addvar = f.groups['Platform'].variables['time3']                            
##                addvar[LoopIndex0]=  Time[0]*100
#
#
#                
#                #Find if the beam group is horizontal or vertical 
#                #This is a temporarly fix, other solution may be applied
#                if diry[0] ==2.8125:
##                    addvardir = f.groups['Sonar'].groups['Beam_group1']
#                    addvardir2 = fid.groups['Sonar'].groups['Beam_group1']
#                    ping = horizontal_ping
##                    go  = True
#                else: 
##                    addvardir = f.groups['Sonar'].groups['Beam_group2']
#                    addvardir2 = fid.groups['Sonar'].groups['Beam_group2']
#                    ping = vertical_ping
##                    go == False
#                
##                if go == True: 
#                #Bug fix to see if there is data avaliable in ping
#                if len(BeamAmplitudeData.shape)==2: 
#                    
#                    
#                    #Go though each beam
#                    for beamnum in range(0,64): 
#                        
##                        #Write beam data
##                        addvar = addvardir.variables['backscatter_r']
##                        addvar[ping,beamnum] = np.array(BeamAmplitudeData[:,beamnum])
##                        addvar = addvardir.variables['backscatter_i']
##                        addvar[ping,beamnum] = np.array(BeamAmplitudeData_imaginary[:,beamnum])
#                        
#                        #Write beam data
#                        addvar = addvardir2.variables['backscatter_r']
#                        addvar[ping,beamnum] = np.array(BeamAmplitudeData[:,beamnum])
#                        addvar = addvardir2.variables['backscatter_i']
#                        addvar[ping,beamnum] = np.array(BeamAmplitudeData_imaginary[:,beamnum])
#                        
#                        
#                    
#                    #Write other sonar data
##                    addvar = addvardir.variables['equivalent_beam_angle']
##                    addvar[ping,:] = 10**(equivalentbeamangle/10)
#                    addvar = addvardir2.variables['equivalent_beam_angle']
#                    addvar[ping,:] = 10**(equivalentbeamangle/10)
#
##                    addvar = addvardir.variables['transducer_gain']
##                    addvar[ping,:] = transducer_gain
#                    addvar = addvardir2.variables['transducer_gain']
#                    addvar[ping,:] = transducer_gain
#
##                    addvar = addvardir.variables['beamwidth_receive_major']
##                    addvar[ping,:] = BWalong
#                    addvar = addvardir2.variables['beamwidth_receive_major']
#                    addvar[ping,:] = BWalong
#
##                    addvar = addvardir.variables['beamwidth_receive_minor']
##                    addvar[ping,:] = BWatwh
#                    addvar = addvardir2.variables['beamwidth_receive_minor']
#                    addvar[ping,:] = BWatwh
#
##                    addvar = addvardir.variables['beamwidth_transmit_major']
##                    addvar[ping,:] = BWalongTX
#                    addvar = addvardir2.variables['beamwidth_transmit_major']
#                    addvar[ping,:] = BWalongTX
#
##                    addvar = addvardir.variables['beamwidth_transmit_minor']
##                    addvar[ping,:] = BWatwhTX
#                    addvar = addvardir2.variables['beamwidth_transmit_minor']
#                    addvar[ping,:] = BWatwhTX
#                    
##                    addvar = addvardir.variables['transmit_bandwidth']
##                    addvar[ping] = bandwidth
#                    addvar = addvardir2.variables['transmit_bandwidth']
#                    addvar[ping] = bandwidth
#                    
##                    addvar = addvardir.variables['sample_interval']
##                    addvar[ping] = sampleinterval
#                    addvar = addvardir2.variables['sample_interval']
#                    addvar[ping] = sampleinterval
#                    
##                    addvar = addvardir.variables['transmit_frequency_start']
##                    addvar[ping] = frequency
#                    addvar = addvardir2.variables['transmit_frequency_start']
#                    addvar[ping] = frequency
#                    
##                    addvar = addvardir.variables['transmit_frequency_stop']
##                    addvar[ping] = frequency
#                    addvar = addvardir2.variables['transmit_frequency_stop']
#                    addvar[ping] = frequency
#                    
##                    addvar = addvardir.variables['transmit_duration_equivalent']
##                    addvar[ping] = pulslength
#                    addvar = addvardir2.variables['transmit_duration_equivalent']
#                    addvar[ping] = pulslength
#                    
##                    addvar = addvardir.variables['transmit_duration_nominal']
##                    addvar[ping] = pulslength
#                    addvar = addvardir2.variables['transmit_duration_nominal']
#                    addvar[ping] = pulslength
#                    
##                    addvar = addvardir.variables['transmit_power']
##                    addvar[ping] =transmitpower
#                    addvar = addvardir2.variables['transmit_power']
#                    addvar[ping] =transmitpower
#                    
##                    addvar = addvardir.variables['sample_time_offset']
##                    addvar[ping] =0.004
#                    addvar = addvardir2.variables['sample_time_offset']
#                    addvar[ping] =0.004
#                    
##                    addvar = addvardir.variables['beam_type']
##                    addvar[ping] =0
#                    addvar = addvardir2.variables['beam_type']
#                    addvar[ping] =0
#                    
##                    addvar = addvardir.variables['transmit_type']
##                    addvar[ping] =transmitmode
#                    addvar = addvardir2.variables['transmit_type']
#                    addvar[ping] =transmitmode
##                    
##                    addvar = addvardir.variables['ping_time']
##                    addvar[ping] = Time[0]*100
#                    addvar = addvardir2.variables['ping_time']
#                    addvar[ping] = Time[0]*100
#                    
##                    addvar = addvardir.variables['beam_direction_x']
##                    addvar[ping,:] = dirx_u
#                    addvar = addvardir2.variables['beam_direction_x']
#                    addvar[ping,:] = dirx_u
#
##                    addvar = addvardir.variables['beam_direction_y']
##                    addvar[ping,:] = diry_u
#                    addvar = addvardir2.variables['beam_direction_y']
#                    addvar[ping,:] = diry_u
#
##                    addvar = addvardir.variables['beam_direction_z']
##                    addvar[ping,:] = dirz_u
#                    addvar = addvardir2.variables['beam_direction_z']
#                    addvar[ping,:] = dirz_u
#                    
##                    addvar=addvardir.variables['beam_stabilisation']
##                    addvar[ping] = 1
#                    addvar=addvardir2.variables['beam_stabilisation']
#                    addvar[ping] = 1
#                    
##                    addvar=addvardir.variables['non_quantitative_processing']
##                    addvar[ping] = NoiseFilter
#                    addvar=addvardir2.variables['non_quantitative_processing']
#                    addvar[ping] = NoiseFilter
#                    
#                    
#                    #For bookeeping
#                    #Use the same beam identificator as above
#                    if diry[0] ==2.8125:
#                        horizontal_ping = horizontal_ping + 1
#                        
#                    else: 
#                        vertical_ping = vertical_ping + 1
#                    
#
#                    
#        #If this was the last file of the file, close the .nc file
#        
#        
#        if horizontal_ping >=maxPingInFile:
#            NumberOfFilesInNC=0
#            Frequency_index = []
#        
#
#        #if last file to be added to .nc
#        if NumberOfFilesInNC >= MaxNumberOfFilesInNC: 
#            NumberOfFilesInNC=0
#        
#        if NumberOfFilesInNC == 0: 
#            
#            
##            f.close()
#            fid.close()
