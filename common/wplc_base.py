from nos.util import ConditionTimeout
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from math import *
from nos.exception import *
import time
import json
import threading


class ADDRESSES:
    #? X
    mig_comparator_less_than    =0o4010
    mig_comparator_greater_than =0o4011

    #? Y
    __broken__          = 0o4000
    __broken__          = 0o4001
    stop                = 0o4002
    __broken__          = 0o4004
    workstation_slider  = 0o4005
    pap1_gripper        = 0o4006
    pap2_gripper        = 0o4007

    mig_trigger         = 0o4010
    laser_trigger       = 0o4010
    test_y              = 0o4017

    #? GY
    start   = 0o0
    stop    = 0o2

    flag_place_next_part        = 0o10
    flag_part_in_place          = 0o11
    flag_return_to_pickup       = 0o12
    mig_comparator_arc_status   = 0o13

    #? V
    part_request_regs=[0o16000, 0o16100, 0o16200, 0o16300, 0o16400, 0o16500, 0o16600, 0o16700, 0o17000, 0o17100, 0o17200, 0o17300]
    
    def __init__(self) -> None:
        pass

addr = ADDRESSES()


class PLCBase(ModbusTcpClient):
    w_msg_len=0o100

    def __init__(self, client, port=502):
        """Initialize the PLC client."""
        self.client = client
        self.port = port
        self.connected = False
        self.lock = threading.Lock()  # Lock for thread-safe operations

    def init(self):
        """Initialize the connection to the PLC."""
        try:
            super().__init__(self.client, self.port)
            self.connected = super().connect()
            if self.connected:
                print('Connected to PLC successfully')
            else: 
                raise ConnectionError('Could not connect to host')
        except Exception as e:
            self.handle_connection_error(e)

    def reconnect(self):
        """Attempt to reconnect to the PLC if the connection is lost."""
        print('Attempting to reconnect to PLC...')
        try:
            self.connected = super().connect()
            if self.connected:
                print('Reconnected to PLC successfully.')
            else:
                raise ConnectionError('Failed to reconnect to PLC')
        except Exception as e:
            self.handle_connection_error(e)

    def is_connection_active(self):
        """Check if the PLC connection is still active."""
        try:
            # Perform a lightweight no-op read (e.g., address 0, one coil)
            response = super().read_coils(0, 1)
            # print(f'is_connection_active: {response}')
            if response is not None and not isinstance(response, Exception):
                return True
            return False
        except Exception as e:
            print(f'Connection validation failed: {e}')
            return False

    def handle_connection_error(self, error):
        """Handle connection errors. Must be implemented by subclasses."""
        raise Error(f'Handle Connection Error: {error}')

    def write_coil(self, address, value, retries=3, delay=0.1, **kwargs):
        # Ensure the connection is active
        if not self.is_connection_active():
            print(f'Connection to PLC is not active. Attempting to reconnect...')
            self.reconnect()
            if not self.is_connection_active():  # Validate again after reconnecting
                print(f'Unable to validate connection after reconnecting. Aborting write_coil({address}, {value}, ...).')
                return None  # Abort the write operation

        # Proceed with the write operation
        with self.lock:
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

    #? read / write
    def read_coil(self, address, retries=3, delay=0.25):
        # Ensure the connection is active
        if not self.is_connection_active():
            print(f'Connection to PLC is not active. Attempting to reconnect...')
            self.reconnect()
            if not self.is_connection_active():  # Validate again after reconnecting
                print(f'Unable to validate connection after reconnecting. Aborting read_coil({address}, ...).')
                return None  # Abort the read operation

        # Proceed with the read operation
        with self.lock:  # Lock to ensure only one thread accesses the PLC
            for attempt in range(retries):
                try:
                    response = super().read_coils(address, 1)
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
    
    def read_discrete(self, address, retries=3, delay=0.25):
        # Ensure the connection is active
        if not self.is_connection_active():
            print(f'Connection to PLC is not active. Attempting to reconnect...')
            self.reconnect()
            if not self.is_connection_active():  # Validate again after reconnecting
                print(f'Unable to validate connection after reconnecting. Aborting read_discrete({address}, ...).')
                return None  # Abort the read operation

        # Proceed with the read operation
        with self.lock:
            for attempt in range(retries):
                try:
                    response = super().read_discrete_inputs(address, 1)
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

    #? Asynchronous versions of read/write methods
    def read_coil_async(self, address, retries=3, delay=0.25, callback=None):
        def async_task():
            result = self.read_coil(address, retries=retries, delay=delay)
            if callback:
                callback(result)
        threading.Thread(target=async_task, daemon=True).start()

    def read_discrete_async(self, address, retries=3, delay=0.25, callback=None):
        def async_task():
            result = self.read_discrete(address, retries=retries, delay=delay)
            # self.read_discrete_inputs()?
            if callback:
                callback(result)
        threading.Thread(target=async_task, daemon=True).start()

    def write_coil_async(self, address, value, retries=3, delay=0.25, callback=None, **kwargs):
        def async_task():
            result = self.write_coil(address, value, retries=retries, delay=delay, **kwargs)
            if callback:
                # print(f'result: {type(result)}')
                callback(result)
        threading.Thread(target=async_task, daemon=True).start()








if __name__=='__main__':
    ip_plc='192.168.69.181'
    plc=PLCBase(ip_plc)
    plc.init()

    # print(plc.read_discrete(addr.mig_comparator_less_than))
    # print(plc.read_discrete(addr.mig_comparator_greater_than))

    taddr = 0o10
    # print(plc.read_discrete(taddr))
    # # plc.write_coil_async(taddr, True)
    # plc.write_coil(taddr, True)
    
    print(plc.read_discrete(taddr))
    # print(plc.read_discrete(taddr))

    # for i in range(5):
    #     print(plc.read_discrete(0o4000))
    #     print(plc.read_coil(addr.start))
    #     print('')
    #     time.sleep(1)



    plc.close()


