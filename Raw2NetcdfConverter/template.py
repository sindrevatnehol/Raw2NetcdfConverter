# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 14:46:29 2018

@author: sindrev
"""

import numpy as np
import pytz, pynmea2, datetime


    
    
def addGlobalAttributes(f,filename)   : 
    '''fuction to set the global variables for the netcdf file'''
    
    
    #Set the time of creation to the .nc file
    filetime=pytz.timezone('Europe/Oslo').localize(datetime.datetime.utcnow())
    
    
    #Write creation of file
    f.Conventions = 'CF-1.7, SONAR-netCDF4, ACDD-1.3'
    #f._NCProperties = 'version=1|netcdflibversion=4.6.1|hdf5libversion=1.8.20'
    f.date_created = str(filetime).replace(' ','T')
    f.keywords = 'Simrad '+filename[:4]
    f.license = 'None'
    f.rights = 'Unrestricted rights'
    f.sonar_convention_authority  = 'ICES'
    f.sonar_convention_name = 'SONAR-netCDF4'
    f.sonar_convention_version  = '1.0'
    f.summary = 'Converted files from .raw format'
    f.title = 'raw to nc converted files'
    
    
    
    

    
def addAnnotation(fid): 
    '''Function to create annotation'''
    
    #Create group
    fid.createGroup('Annotation')
    
    
    #Create time dimension
    fid.groups['Annotation'].createDimension('time',None)
    
    
    #Create annotaiton txt
    annotationTxt = fid.groups['Annotation'].createVariable('annotation_text',str,('time',), chunksizes = (512,))
    annotationTxt.long_name = 'Annotaton text'

    #Create annotation category    
    annotationTxt = fid.groups['Annotation'].createVariable('annotation_category',str,('time',), chunksizes = (512,))
    annotationTxt.long_name = 'Annotation category'
    
    
    #Make time into variable and add attributes
    time = fid.groups['Annotation'].createVariable('time',np.uint64,('time',), chunksizes = (512,))
    #time.NAME = 'time'
    time.axis = 'T'
    time.calendar = 'gregorian'
    time.long_name = 'Timestamps of annotations'
    time.standard_name = 'time'
    time.units = 'nanoseconds since 1601-01-01 00:00:00Z'
    
    
    
def addEnvironment(fid): 
    '''Function to create environment group'''
    fid.createGroup('Environment')
    
    #create dimension frequency
    fid.groups['Environment'].createDimension('frequency',None)

    
    #Create absorption indicative variable with attributes
    abso = fid.groups['Environment'].createVariable('absorption_indicative',np.float32,('frequency',), chunksizes = (512,))
    abso.long_name = 'Indicative acoustic absorption'
    abso.units = 'dB/m'
    abso.valid_min = '0.0'

    
    #Create sound_speed_indicative variable with attributes
    snd = fid.groups['Environment'].createVariable('sound_speed_indicative',np.float32,('frequency',), chunksizes = (512,))
    snd.long_name = 'Indicative sound speed'
    snd.standard_name = 'speed_of_sound_in_sea_water'
    snd.units = 'm/s'
    snd.valid_min = '0.0'
    
    
    #Create frequency variable with attributes
    freq = fid.groups['Environment'].createVariable('frequency',np.float32,('frequency',),chunksizes = (512,))
    
#    freq.chunksizes = 1
    #freq.NAME = 'frequency'
    freq.long_name = 'Acoustic frequency'
    freq.standard_name = 'sound_frequency'
    freq.units = 'Hz'
    freq.valid_min = '0.0'
    
    
    
    
    
    
    
    
    
    
    
def addPlatform(fid,platform_code, platform_name, platform_type,f): 
    '''Function to create teh platform group'''
    
    
    
    
    
        
    def copyVariable(varin,varout): 
        '''Function to copy varibales with attribtues'''
        
        varout.createVariable(varin.name, varin.datatype, varin.dimensions, chunksizes = (512,))
        varout.variables[varin.name].setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})
    

    
    
    
    
    
    #Create the platform group with attributes
    fid.createGroup('Platform')
    grp = fid.groups['Platform']
    grp.platform_code_ICES = platform_code
    grp.platform_name = platform_name
    grp.platform_type = platform_type
    
    
    #Create a sub-group named NMEA wiht attributes
    grp.createGroup('NMEA')
    grp2 = grp.groups['NMEA']
    grp2.description = 'All NMEA sensor datagrams'
    
    
    #Create time dimension in subgroup
    grp2.createDimension('time',None)
    
    
    #Create variable in subgroup
    grp2.createVariable('NMEA_datagram',np.str,('time'), chunksizes = (512,))
    grp2.variables['NMEA_datagram'].long_name = 'NMEA datagram'

        
    #create time variable in subgroup
    time = grp2.createVariable('time',np.uint64,('time',), chunksizes = (512,))
    #time.NAME = 'time'
    time.axis = 'T'
    time.calendar = 'gregorian'
    time.long_name = 'Timestamps for NMEA datagrams'
    time.standard_name = 'time'
    time.units = 'nanoseconds since 1601-01-01 00:00:00Z'
    
    
    #Copy some constants, pynetcdf does not create constants
    copyVariable(f.groups['Platform'].variables['MRU_offset_x'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['MRU_offset_y'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['MRU_offset_z'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['MRU_rotation_x'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['MRU_rotation_y'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['MRU_rotation_z'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['position_offset_x'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['position_offset_y'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['position_offset_z'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['transducer_offset_x'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['transducer_offset_y'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['transducer_offset_z'],fid.groups['Platform'])
    copyVariable(f.groups['Platform'].variables['water_level'],fid.groups['Platform'])
    
    
    
    


def writePlatformData(FileData,GPSsourceList,fid):
    '''Function to write the platform data'''
    
    
    
                
    def makeMRUvariable(time,grp): 
        
        
        grp.createDimension(time,None)
        
        grp.createVariable('vertical_offset',np.float32,(time,), chunksizes = (512,))
        var = grp.variables['vertical_offset']
        var.long_name = 'Platform vertical offset from nominal'
        var.units = 'm'
        
        grp.createVariable('roll',np.float32,(time,), chunksizes = (512,))
        var = grp.variables['roll']
        var.long_name = 'Platform roll'
        var.standard_name = 'platform_roll_angle'
        var.units = 'arc_degree'
        var.valid_range = np.array((-180.0,180.0))
        
        grp.createVariable('pitch',np.float32,(time,), chunksizes = (512,))
        var = grp.variables['pitch']
        var.long_name = 'Platform pitch'
        var.standard_name = 'platform_pitch_angle'
        var.units = 'arc_degree'
        var.valid_range = np.array((90.0,90.0))
        
        
        
        time_var = grp.createVariable(time,np.uint64,(time,), chunksizes = (512,))
     #   time_var.NAME = time
        time_var.axis = 'T'
        time_var.calendar = 'gregorian'
        time_var.long_name = 'Timestamps for MRU data'
        time_var.standard_name = 'time'
        time_var.units = 'nanoseconds since 1601-01-01 00:00:00Z'
        
        
        
        
    def makeHeadingVariable(time,grp): 
    
        
        name = time
        addvar = grp
        long_name = 'Timestamps for gyrocompass data'
    
        addvar.createDimension(name,None)
        
        
        grp.createVariable('heading',np.float32,(time,), chunksizes = (512,))
        
        var = grp.variables['heading']
        var.long_name = 'Platform heading (true)'
        var.standard_name = 'platform_orientation'
        var.units = 'degrees_north'
        var.valid_range = np.array((0.0,360.0))
            
        
        
        time_var = addvar.createVariable(name,np.uint64,(name,), chunksizes = (512,))
      #  time_var.NAME = name
        time_var.axis = 'T'
        time_var.calendar = 'gregorian'
        time_var.long_name = long_name
        time_var.standard_name = 'time'
        time_var.units = 'nanoseconds since 1601-01-01 00:00:00Z'
        
        
       
    def createPositionData(grp,time): 
        
        name = time
        addvar = grp
        long_name = 'Timestamps for position data'
        
        addvar.createDimension(name,None)
        
        
        
        
        grp.createVariable('latitude',np.float64,(time,), chunksizes = (512,))
        
        var= grp.variables['latitude']
        var.long_name = 'Platform latitude'
        var.standard_name = 'latitude'
        var.units = 'degrees_north'
        var.valid_range = np.array((-90.0,90.0))
        
        
        grp.createVariable('longitude',np.float64,(time,), chunksizes = (512,))
        var= grp.variables['longitude']
        var.long_name = 'Platform longitude'
        var.standard_name = 'longitude'
        var.units = 'degrees_east'
        var.valid_range = np.array((-180.0,180.0))
        
        
        grp.createVariable('speed_ground',np.float32,(time,), chunksizes = (512,))
        var= grp.variables['speed_ground']
        var.long_name = 'Platform speed over ground'
        var.standard_name = 'platform_speed_wrt_ground'
        var.units = 'm/s'
        var.valid_min = '0.0'
        
        
        grp.createVariable('speed_relative',np.float32,(time,), chunksizes = (512,))
        var= grp.variables['speed_relative']
        var.long_name = 'Platform speed relative to water'
        var.standard_name = 'platform_speed_wrt_seawater'
        var.units = 'm/s'
        var.valid_min = '0.0'
        
    
        time_var = addvar.createVariable(name,np.uint64,(name,), chunksizes = (512,))
       # time_var.NAME = name
        time_var.axis = 'T'
        time_var.calendar = 'gregorian'
        time_var.long_name = long_name
        time_var.standard_name = 'time'
        time_var.units = 'nanoseconds since 1601-01-01 00:00:00Z'
        
        
        
    #Some bookkeeping
    timeIndex = 1
    LoopIndex1 =0
    LoopIndexHeading = 0
    positionTime = []
    headingTime = []
    positionOldTime = 0
    headingOldTime = 0
    
    
    #Get the correct group
    grp = fid.groups['Platform']


    #Loop through each nmea information
    for LoopIndex0 in range(len(FileData.NMEA_time)): 
        
        
        #Get telegram and its time of occurence
        Time = int(FileData.NMEA_time[LoopIndex0][0])*100
        info = FileData.NMEA_info[LoopIndex0]
        

        #store the nmea data
        grp.groups['NMEA'].variables['NMEA_datagram'][LoopIndex0] = info
        grp.groups['NMEA'].variables['time'][LoopIndex0] = Time
        


        try: 
            #Parse nmea string
            msg = pynmea2.parse(info,check= False)  

            
            #Only use one gps telegram. 
            if info.split(',')[0][-3:]==GPSsourceList[0]: 
                
            
                try: 
                    try: 
                        #Try this to see if the telegram is ok (data bug)
                        msg.latitude + msg.longitude
                        
                        
                        #If both lat and lon equals 0 (data bug)
                        if msg.latitude == 0 and msg.longitude == 0: 
                            grp.variables['latitude'][LoopIndex1]=  np.nan
                            grp.variables['longitude'][LoopIndex1]=  np.nan

                        #Ignore data if the time is repeating
                        elif Time == positionOldTime: 
                            k=1
                            
                        #Otherwise write the lat and lon
                        else:                             
                            grp.variables['latitude'][LoopIndex1]=  msg.latitude
                            grp.variables['longitude'][LoopIndex1]=  msg.longitude

                            #If speed_ground exist write this
                            try: 
                                grp.variables['speed_ground'][LoopIndex1]=  msg.spd_ground
                            except AttributeError: 
                                k=1
                                
                            #Write time variable
                            grp.variables[positionTime][LoopIndex1]=  Time


                            #Something for bookkeeping
                            positionOldTime = Time
                            LoopIndex1 = LoopIndex1+1
                    except AttributeError: 
                        k=1
                        
                #If the variable does not exist, create it
                except KeyError:                
                    
                    #create variable
                    createPositionData(grp,'time'+str(timeIndex))
                    
                    #Set the name of the time variable
                    positionTime = 'time'+str(timeIndex)
                    timeIndex = timeIndex+1
                    
                    #write the lat lon data
                    grp.variables['latitude'][LoopIndex1]=  msg.latitude
                    grp.variables['longitude'][LoopIndex1]=  msg.longitude

                    #write the speed data
                    try: 
                        grp.variables['speed_ground'][LoopIndex1]=  msg.spd_ground
                    except AttributeError: 
                        k=1
                        
                    #write time data
                    grp.variables[positionTime][LoopIndex1]=  Time

                    
                    #Something for bookkeeping
                    positionOldTime = Time
                    LoopIndex1 = LoopIndex1+1
            
            
            #Heading
            try: 
                #Check if heading information is ok (data bug)
                msg.heading
                
                
                #If first heading information
                if LoopIndexHeading == 0:
                    
                    #Set the name of the time dimension
                    headingTime = 'time'+str(timeIndex)
                    timeIndex = timeIndex+1
                    
                    #Make the variables 
                    makeHeadingVariable(headingTime,grp)
                
                if Time != headingOldTime: 
                    try:  
                        #Add the heading and time information
                        grp.variables['heading'][LoopIndexHeading] = msg.heading
                        grp.variables[headingTime][LoopIndexHeading] = Time

                        #Somehting for bookkeeping
                        headingOldTime = Time    
                        LoopIndexHeading = LoopIndexHeading+1
                    except ValueError: 
                        k=1
            except AttributeError: 
                k=1
                

        except pynmea2.nmea.ParseError: 
            k=1
            
            
    oldMRUTime = 0
    for LoopIndex0 in range(len(FileData.NMEA)): 
        
        Time = FileData.NMEA[LoopIndex0][0]

        if LoopIndex0 ==0: 
            mruTime = 'time'+str(timeIndex)
            timeIndex = timeIndex+1
        
            makeMRUvariable(mruTime,grp)
        
        
        if Time != oldMRUTime: 
            grp.variables['vertical_offset'][LoopIndex0] = FileData.PingData[LoopIndex0].heave[0]
            grp.variables['roll'][LoopIndex0] = FileData.PingData[LoopIndex0].roll[0]
            grp.variables['pitch'][LoopIndex0] = FileData.PingData[LoopIndex0].pitch[0]
            grp.variables[mruTime][LoopIndex0] = Time
            oldMRUTime = Time
                
                        
    

    
def addProvenance(fid): 
    fid.createGroup('Provenance')
    
    prov = fid.groups['Provenance']
    prov.conversion_software_name = 'P_IMR_RAW_2_NETCDF4'
    prov.conversion_software_version = '1.0.0'
    prov.conversion_time = '2018-04-12 15:50:06.205532+02:00'
    
    
    prov.createDimension('filenames',None)
    prov.createVariable('filenames',np.float32,'filenames', chunksizes = (512,))
    
    src = prov.variables['filenames']
#    src.NAME ='This is a netCDF dimension but not a netCDF variable.         0'
    
    prov.createVariable('source_filenames',str,'filenames', chunksizes = (512,))
    var = prov.variables['source_filenames']
    var.long_name = ' Source filenames'
    
    
    

    
def createSonarData(fid): 
    fid.createGroup('Sonar')

    sonar = fid.groups['Sonar']


    enum_dict_stab = {u'not_stabilised': 0, u'stabilised': 1}
    beam_stabilisation_t=sonar.createEnumType(np.uint8,'beam_stabilisation_t',enum_dict_stab)
    
    enum_dict = {u'single': 0, u'split_aperture': 1}
    beam_t=sonar.createEnumType(np.uint8,'beam_t',enum_dict)
    
    enum_dict = {u'type_1': 1, u'type_2': 2}
    conversion_equation_t=sonar.createEnumType(np.uint8,'conversion_equation_t',enum_dict)
    
    sample_t = sonar.createVLType(np.float32,'sample_t')
    
    enum_dict = {u'CW': 0, u'LFM': 1,u'HFM' :2}
    transmit_t=sonar.createEnumType(np.uint8,'transmit_t',enum_dict)
    
        

    for i in range(2): 
        sonar.createGroup('Beam_group'+str(i+1))
        
        
        sgrp = sonar.groups['Beam_group'+str(i+1)]

        if i == 0: 
            sgrp.beam_mode = 'Horizontal'
        else: 
            sgrp.beam_mode = 'Vertical'
            
        sgrp.conversion_equation_type = 1

        
        
        
    
        sgrp.createDimension('beam',64)
        sgrp.createVariable('beam',str,'beam')
        beam = sgrp.variables['beam']
 #       beam.NAME = 'beam'
        beam.long_name = 'Beam Name'
        
        
        name = 'ping_time'
        addvar = sgrp
    
        addvar.createDimension(name,None)
        
    
    
    
        sgrp.createVariable('backscatter_i',sample_t,('ping_time','beam'))
        back = sgrp.variables['backscatter_i']
        back.long_name = 'Raw backscatter measurements (imaginary part)'
        back.units = 'VA'
    
        sgrp.createVariable('backscatter_r',sample_t,('ping_time','beam'))
        back = sgrp.variables['backscatter_r']
        back.long_name = 'Raw backscatter measurements (real part)'
        back.units = 'VA'
    
        sgrp.createVariable('beam_direction_x',np.float32,('ping_time','beam'))
        back = sgrp.variables['beam_direction_x']
        back.long_name = 'x-component of the vector that gives the pointing direction of the beam, in sonar beam coordinate system'
        back.units = '1'
        back.valid_range = np.array((-1.0,1.0))
        
        sgrp.createVariable('beam_direction_y',np.float32,('ping_time','beam'))
        back = sgrp.variables['beam_direction_y']
        back.long_name = 'y-component of the vector that gives the pointing direction of the beam, in sonar beam coordinate system'
        back.units = '1'
        back.valid_range = np.array((-1.0,1.0))
    
        sgrp.createVariable('beam_direction_z',np.float32,('ping_time','beam'))
        back = sgrp.variables['beam_direction_z']
        back.long_name = 'z-component of the vector that gives the pointing direction of the beam, in sonar beam coordinate system'
        back.units = '1'
        back.valid_range = np.array((-1.0,1.0))
    
        sgrp.createVariable('beam_stabilisation',beam_stabilisation_t,('ping_time',),chunksizes = (512,))
        back = sgrp.variables['beam_stabilisation']
        back.long_name = 'Beam stabilisation applied (or not)'
    
        sgrp.createVariable('beam_type',beam_t,('ping_time',),chunksizes = (512,))
        back = sgrp.variables['beam_stabilisation']
        back.long_name = 'Type of beam'
    
        sgrp.createVariable('beamwidth_receive_major',np.float32,('ping_time','beam'))
        back = sgrp.variables['beamwidth_receive_major']
        back.long_name = 'Half power one-way receive beam width along major (horizontal) axis of beam'
        back.units='arc_degree'
        back.valid_range = np.array((0.0,360.0))
    
        sgrp.createVariable('beamwidth_receive_minor',np.float32,('ping_time','beam'))
        back = sgrp.variables['beamwidth_receive_minor']
        back.long_name = 'Half power one-way receive beam width along minor (vertical) axis of beam'
        back.units='arc_degree'
        back.valid_range = np.array((0.0,360.0))
    
        sgrp.createVariable('beamwidth_transmit_major',np.float32,('ping_time','beam'))
        back = sgrp.variables['beamwidth_transmit_major']
        back.long_name = 'Half power one-way transmit beam width along major (horizontal) axis of beam'
        back.units='arc_degree'
        back.valid_range = np.array((0.0,360.0))
    
        sgrp.createVariable('beamwidth_transmit_minor',np.float32,('ping_time','beam'))
        back = sgrp.variables['beamwidth_transmit_minor']
        back.long_name = 'Half power one-way transmit beam width along minor (vertical) axis of beam'
        back.units='arc_degree'
        back.valid_range = np.array((0.0,360.0))
    
        sgrp.createVariable('equivalent_beam_angle',np.float32,('ping_time','beam'))
        back = sgrp.variables['equivalent_beam_angle']
        back.long_name = 'Equivalent beam angle'
        back.units='sr'
        back.valid_range = np.array((0.0,12.566371))
    
        sgrp.createVariable('gain_correction',np.float32,('ping_time','beam'))
        back = sgrp.variables['gain_correction']
        back.long_name = 'Gain correction'
        back.units='dB'
    
        sgrp.createVariable('non_quantitative_processing',np.int16,('ping_time',),chunksizes = (512,))
        back = sgrp.variables['non_quantitative_processing']
        back.flag_meanings = 'no_non_quantitative_processing simrad_weak_noise_filter simrad_medium_noise_filter simrad_strong_noise_filter'
        back.flag_values = '0, 1, 2, 3'
        back.long_name = 'Presence or not of non-quantitative processing applied to the backscattering data (sonar specific)'
    
        sgrp.createVariable('receiver_sensitivity',np.float32,('ping_time','beam'))
        back = sgrp.variables['receiver_sensitivity']
        back.long_name = 'Receiver sensitivity'
        back.units = 'dB re 1/uPa'

        sgrp.createVariable('sample_interval',np.float32,('ping_time',),chunksizes = (512,))
        back = sgrp.variables['sample_interval']
        back.long_name = ' Interval between recorded raw data samples'
        back.units = 's'
        back.valid_min = '0.0'
    
        sgrp.createVariable('sample_time_offset',np.float32,('ping_time',),chunksizes = (512,))
        back = sgrp.variables['sample_time_offset']
        back.long_name = 'Time offset that is subtracted from the timestamp of each sample'
        back.units = 's'
    
        sgrp.createVariable('time_varied_gain',sample_t,('ping_time',),chunksizes = (512,))
        back = sgrp.variables['time_varied_gain']
        back.long_name = 'Time-varied-gain coefficients'
        back.units = 'dB'
    
        sgrp.createVariable('transducer_gain',np.float32,('ping_time','beam'))
        back = sgrp.variables['transducer_gain']
        back.long_name = 'Gain of transducer'
        back.units = 'dB'
    
        sgrp.createVariable('transmit_bandwidth',np.float32,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_bandwidth']
        back.long_name = 'Nominal bandwidth of transmitted pulse'
        back.units = 'Hz'
        back.valid_min = '0.0'
    
        sgrp.createVariable('transmit_duration_equivalent',np.float32,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_duration_equivalent']
        back.long_name = 'Equivalent duration of transmitted pulse'
        back.units = 's'
        back.valid_min = '0.0'
    
        sgrp.createVariable('transmit_duration_nominal',np.float32,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_duration_nominal']
        back.long_name = 'Nominal duration of transmitted pulse'
        back.units = 's'
        back.valid_min = '0.0'
    
        sgrp.createVariable('transmit_frequency_start',np.float32,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_frequency_start']
        back.long_name = ' Start frequency in transmitted pulse'
        back.standard_name = 'sound_frequency'
        back.units = 'Hz'
        back.valid_min = '0.0'
    
        sgrp.createVariable('transmit_frequency_stop',np.float32,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_frequency_stop']
        back.long_name = 'Stop frequency in transmitted pulse'
        back.standard_name = 'sound_frequency'
        back.units = 'Hz'
        back.valid_min = '0.0'
    
        sgrp.createVariable('transmit_power',np.float32,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_power']
        back.long_name = 'Nominal transmit power'
        back.units = 'W'
        back.valid_min = '0.0'
#    
        sgrp.createVariable('transmit_source_level',np.float32,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_source_level']
        back.long_name = 'Transmit source level'
        back.units = 'dB re 1 uPa at 1m'
    
        sgrp.createVariable('transmit_type',transmit_t,('ping_time'),chunksizes = (512,))
        back = sgrp.variables['transmit_type']
        back.long_name = 'Type of transmitted pulse'

        
        time_var = addvar.createVariable(name,np.uint64,(name,),chunksizes = (512,))
  #      time_var.NAME = name
        time_var.axis = 'T'
        time_var.calendar = 'gregorian'
        time_var.long_name = 'Timestamp of each ping'
        time_var.standard_name = 'time'
        time_var.units = 'nanoseconds since 1601-01-01 00:00:00Z'
        
        
    
def addVendorSpecificGrp(fid): 
    fid.createGroup('Vendor_specific')
    


    
    
def addEnvironmentData(FileData, fid): 
    
    Frequency_index = []
    
     #Loop through every ping in raw fil
    for LoopIndex0 in range(0,len(FileData.PingData)): 
        
        
        #If there is information inside the ping continue
        if not FileData.NMEA[LoopIndex0] ==[]:
            
            frequency = FileData.PingData[LoopIndex0].frequency[0]       

            absorption = FileData.PingData[LoopIndex0].absorptioncoefficient[0]

            soundvelocity = FileData.PingData[LoopIndex0].soundvelocity[0]

            #Get all unique frequencies and store it
            if not frequency in Frequency_index: 

                Frequency_index = np.hstack((Frequency_index,frequency))
               #Write Environment information
                fid.groups['Environment'].variables['frequency'][len(Frequency_index)-1]=frequency
                fid.groups['Environment'].variables['absorption_indicative'][len(Frequency_index)-1]=absorption
                fid.groups['Environment'].variables['sound_speed_indicative'][len(Frequency_index)-1]=soundvelocity



def addSonarData(FileData,fid,transducer_rotation): 
    
    horizontal_ping =0
    vertical_ping = 0
    
    #Loop through every ping in raw fil
    for LoopIndex0 in range(0,len(FileData.PingData)): 
        
        
        #If there is information inside the ping continue
        if not FileData.NMEA[LoopIndex0] ==[]:
            
            
            #Get the time of the ping from nmea
            Time = FileData.NMEA[LoopIndex0]
            

            #Get relevant information from raw data
            sampleinterval = FileData.PingData[LoopIndex0].sampleinterval[0]

            frequency = FileData.PingData[LoopIndex0].frequency[0]                  

            transmitpower = FileData.PingData[LoopIndex0].transmitpower[0]       

            pulslength = FileData.PingData[LoopIndex0].pulslength[0]     

#                bandwidth = FileData.PingData[LoopIndex0].bandwidth[0] 

            transducer_gain = FileData.PingData[LoopIndex0].gainrx+FileData.PingData[LoopIndex0].gaintx
            
            transmitmode = FileData.PingData[LoopIndex0].transmitmode[0]

            dirx = FileData.PingData[LoopIndex0].dirx

            diry = FileData.PingData[LoopIndex0].diry

            equivalentbeamangle = FileData.PingData[LoopIndex0].equivalentbeamangle

            BeamAmplitudeData =  FileData.PingData[LoopIndex0].BeamAmplitudeData
            
            BeamAmplitudeData_imaginary =  FileData.PingData[LoopIndex0].BeamAmplitudeData_imaginary


            BWalong = FileData.PingData[LoopIndex0].beamwidthalongshiprx
            
            BWatwh=FileData.PingData[LoopIndex0].beamwidthathwartshiprx

            BWalongTX = FileData.PingData[LoopIndex0].beamwidthhorizontaltx[0]

            BWatwhTX=FileData.PingData[LoopIndex0].beamwidthverticaltx[0]

            NoiseFilter=FileData.PingData[LoopIndex0].noisefilter[0]

           
            #Convert beam direction into unit vectors
            dirx_u = np.cos((dirx)*np.pi/180)*np.cos((diry+transducer_rotation[0])*np.pi/180)
            
            diry_u = np.cos((dirx)*np.pi/180)*np.sin((diry+transducer_rotation[0])*np.pi/180)
            
            dirz_u = np.sin((dirx)*np.pi/180)
            
            

            
            #Find if the beam group is horizontal or vertical 
            #This is a temporarly fix, other solution may be applied
            if diry[0] ==2.8125:
                addvardir2 = fid.groups['Sonar'].groups['Beam_group1']
                ping = horizontal_ping
            else: 
                addvardir2 = fid.groups['Sonar'].groups['Beam_group2']
                ping = vertical_ping
                
                
            #Bug fix to see if there is data avaliable in ping
            if len(BeamAmplitudeData.shape)==2: 
                
                
                #Go though each beam
                for beamnum in range(0,64): 
                    #Write beam data
                    addvar = addvardir2.variables['backscatter_r']
                    try: 
                        addvar[ping,beamnum] = np.array(BeamAmplitudeData[:,beamnum])
                    except IndexError:
                        addvar[ping,beamnum] = np.array(np.float32(np.nan))#np.array(np.ones(addvar[:,0].shape))

                    addvar = addvardir2.variables['backscatter_i']
                    try: 
                        addvar[ping,beamnum] = np.array(BeamAmplitudeData_imaginary[:,beamnum])
                    except IndexError: 
                        addvar[ping,beamnum] = np.array(np.float32(np.nan))#np.ones(addvar[:,0].shape))
                    
                
                #Write other sonar data
                addvar = addvardir2.variables['equivalent_beam_angle']
                try: 
                    addvar[ping,:] = 10**(equivalentbeamangle/10)
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transducer_gain']
                try: 
                    addvar[ping,:] = transducer_gain
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beamwidth_receive_major']
                try: 
                    addvar[ping,:] = BWalong
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beamwidth_receive_minor']
                try: 
                    addvar[ping,:] = BWatwh
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beamwidth_transmit_major']
                try: 
                    addvar[ping,:] = BWalongTX
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beamwidth_transmit_minor']
                try: 
                    addvar[ping,:] = BWatwhTX
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transmit_bandwidth']
                addvar = addvardir2.variables['sample_interval']
                try: 
                    addvar[ping] = sampleinterval
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transmit_frequency_start']
                try: 
                    addvar[ping] = frequency
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transmit_frequency_stop']
                try: 
                    addvar[ping] = frequency
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transmit_duration_equivalent']
                try: 
                    addvar[ping] = pulslength
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transmit_duration_nominal']
                try: 
                    addvar[ping] = pulslength
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transmit_power']
                try: 
                    addvar[ping] =transmitpower
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['sample_time_offset']
                try: 
                    addvar[ping] =0.004
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beam_type']
                try: 
                    addvar[ping] =0
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['transmit_type']
                try: 
                    addvar[ping] =transmitmode
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['ping_time']
                try: 
                    addvar[ping] = Time
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beam_direction_x']
                try: 
                    addvar[ping,:] = dirx_u
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beam_direction_y']
                try: 
                    addvar[ping,:] = diry_u
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar = addvardir2.variables['beam_direction_z']
                try: 
                    addvar[ping,:] = dirz_u
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar=addvardir2.variables['beam_stabilisation']
                try: 
                    addvar[ping] = 1
                except ValueError: 
                    addvar[ping,:] = np.nan
                addvar=addvardir2.variables['non_quantitative_processing']
                try: 
                    addvar[ping] = NoiseFilter
                except ValueError: 
                    addvar[ping,:] = np.nan
                
                
                #For bookeeping
                #Use the same beam identificator as above
                if diry[0] ==2.8125:
                    horizontal_ping = horizontal_ping + 1
                    
                else: 
                    vertical_ping = vertical_ping + 1
                    
                
                
                
    
    
    
    
    
