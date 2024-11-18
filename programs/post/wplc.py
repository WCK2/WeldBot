from nos.util import ConditionTimeout
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from math import *
from nos.exception import *
import time
import json


class ADDRESSES:
    #? X
    mig_comparator_less_than    =0o4010
    mig_comparator_greater_than =0o4011

    #? Y
    stop                =0o4002
    workstation_slider  =0o4005
    pap1_gripper        =0o4006
    pap2_gripper        =0o4007

    mig_trigger         =0o4010
    laser_trigger       =0o4010

    #? GY
    start=0o0

    flag_place_next_part        =0o10
    flag_part_in_place          =0o11
    flag_return_to_pickup       =0o12
    mig_comparator_arc_status   =0o13

    #? V
    part_request_regs=[0o16000, 0o16100, 0o16200, 0o16300, 0o16400, 0o16500, 0o16600, 0o16700, 0o17000, 0o17100, 0o17200, 0o17300]
    
    def __init__(self) -> None:
        pass

addr=ADDRESSES()


class PLC(ModbusTcpClient):
    w_msg_len=0o100
    def __init__(self, client, port=502):
        """ ip (`str`): ip address """
        self.client=client
        self.port=port
        self.connected=False

    def init(self):
        try:
            super().__init__(self.client, self.port)
            self.connected=super().connect()
            if not self.connected: raise Error('Could not connect to host')
        except:
            raise Error('Modbus connection initialization failed')

    #? read / write
    def read_coil(self, address, retires=3, delay=0.25):
        for attempt in range(retires):
            try:
                response=super().read_coils(address, 1)
                if isinstance(response, ModbusIOException):
                    print(f'ModbusIOException encountered at address {address} on attempt {attempt+1}')
                    time.sleep(delay)
                    continue
                return response.bits[0]
            except AttributeError as e:
                print(f'AttributeError on attempt {attempt+1}: {e}')
                time.sleep(delay)
                continue
            except Exception as e:
                print(f'Unexpected error on attempt {attempt+1}: {e}')
                time.sleep(delay)
                continue
        return None
    
    def read_discrete(self, address, retires=3, delay=0.25):
        for attempt in range(retires):
            try:
                response=super().read_discrete_inputs(address, 1)
                if isinstance(response, ModbusIOException):
                    print(f'ModbusIOException encountered at address {address} on attempt {attempt+1}')
                    time.sleep(delay)
                    continue
                return response.bits[0]
            except AttributeError as e:
                print(f'AttributeError on attempt {attempt+1}: {e}')
                time.sleep(delay)
                continue
            except Exception as e:
                print(f'Unexpected error on attempt {attempt+1}: {e}')
                time.sleep(delay)
                continue
        return None

    def write_coil(self, address, value, retries=3, delay=0.1, **kwargs):
        for attempt in range(retries):
            try:
                response = super().write_coil(address, value, **kwargs)
                if isinstance(response, ModbusIOException):
                    print(f'ModbusIOException encountered at address {address} on attempt {attempt+1}')
                    time.sleep(delay)
                    continue
                return response
            except AttributeError as e:
                print(f'AttributeError on attempt {attempt+1}: {e}')
                time.sleep(delay)
                continue
            except Exception as e:
                print(f'Unexpected error on attempt {attempt+1}: {e}')
                time.sleep(delay)
                continue
        return None




if __name__=='__main__':
    ip_plc='192.168.69.181'
    plc=PLC(ip_plc)
    plc.init()

    print(plc.read_discrete(addr.mig_comparator_less_than))
    print(plc.read_discrete(addr.mig_comparator_greater_than))

    # print(plc.read_msg(addr.part_request_regs[0]))
    # print(plc.part_requests)
    # plc.part_requests=[['CanadaMS3', 'LockEyelet', 0], ['CanadaMS3', 'LockEyelet', 1], ['CanadaMS3', 'LockEyelet', 2], ['CanadaMS3', 'LockEyelet', 3], ['CanadaMS3', 'SwitchMountPlate', 0], ['CanadaMS3', 'LHBracket', 0], ['CanadaMS3', 'HingePlateB0', 0], ['CanadaMS3', 'HingePlateB1', 0]]


    plc.close()


