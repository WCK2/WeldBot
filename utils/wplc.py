from common.wplc_base import *


class PLC(PLCBase):
    def handle_connection_error(self, error):
        """Log connection errors instead of raising exceptions."""
        print(f'Raspberry Pi PLC connection error: {error}')





if __name__=='__main__':
    ip_plc='192.168.69.181'
    plc=PLC(ip_plc)
    plc.init()

    # print(plc.read_discrete(addr.mig_comparator_less_than))
    # print(plc.read_discrete(addr.mig_comparator_greater_than))

    taddr = 0o10
    # print(plc.read_discrete(taddr))
    # # plc.write_coil_async(taddr, True)
    # plc.write_coil(taddr, True)
    
    # print(plc.read_discrete(taddr))
    # print(plc.read_discrete(taddr))

    for i in range(1):
        print(plc.read_discrete(0o4000))
        print(plc.read_coil(addr.start))
        print('')
        time.sleep(1)


    plc.close()


