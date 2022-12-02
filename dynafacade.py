from dynamixel_sdk import *

# This is the facade class The user will control their servos using this.
class ServoController:
    port_handler = None
    packet_handler_protocol_1 = PacketHandler(1)
    packet_handler_protocol_2 = PacketHandler(2)
    servos = None
    # Constructor
    def __init__(self, device_name) -> None:
        self.connect(device_name)
        self.servos = dict()

    def connect(self, device_name):
        self.port_handler = PortHandler(device_name)
        if(self.port_handler.openPort()):
            print(device_name + " Connected.")
        else:
            print("Failed to connect to " + device_name)
            quit()
        self.port_handler.setBaudRate(57_600)
        
    def disconnect(self):
        self.port_handler.closePort()
        print("Port disconnected successfully.")
    
    # Allows a user to add a servo to the controller
    def add_servo(self, new_servo):
        new_servo.packet_handler = self.get_protocol(new_servo.id)
        self.servos[new_servo.id]= new_servo
    
    # Factory function allowing user to create new servo object by specifying an ID and config file.
    def create_servo(self, id, config):
        servo = DynamixelServo(id)
        servo.load_config(config, self.port_handler)
        if(servo.protocol_version == 2):
            servo.packet_handler = self.packet_handler_protocol_2
        else:
            servo.packet_handler = self.packet_handler_protocol_1
        self.servos[id] = servo


    # Displays servo status
    def show_status(self, servo_id):
        servo = self.servos[servo_id]
        print(servo.get_status())

    # displays the status of all servos in the controller
    def show_status_all(self):
        for each_servo in self.servos:
            self.show_status(each_servo.id)

    def get_servo(self, servo_id):
        return self.servos[servo_id]

    # Gets the appropriate packet handler for the given protocol ID
    def get_protocol(self, protocol_id):
        if(protocol_id == 2):
            return self.packet_handler_protocol_2
        elif(protocol_id == 1):
            return self.packet_handler_protocol_1

# This object gets its data from a config file
class DynamixelServo:
    EEPROM = None # String(name): Register
    RAM = None
    STATUS = None
    protocol_version = 2
    packet_handler = None
    
    def __init__(self, servo_id) -> None:
        self.id = servo_id
        self.EEPROM = dict()
        self.RAM = dict()
        self.STATUS = []

    # This loads a servo configuration from a file. This config file will not set the id of the servo but serves as a prototype.
    def load_config(self, filepath, port_handler):
        f = open(filepath, 'r')
        lines = f.readlines()
        f.close()
        protocol = int(lines[0])
        breakchar = lines[1][0]
        self.protocol_version = protocol
        print("protocol:" + str(protocol))
        print("Loading Register tables...")
        register_definitions = lines[2:]
        register_set = self.EEPROM
        i = 0
        for each_definition in register_definitions:
            if(each_definition == '\n'):
                register_set = self.RAM
                continue
            if(each_definition == 'getstatus'):
                self.setup_status(register_definitions[i:])
                break
            breakout = each_definition.split(breakchar) 
            address = breakout[0]
            size = breakout [1]
            name = breakout [2]
            access = breakout[3]
            reg = Register(name, address, size, access, protocol,port_handler,self.id)
            register_set[name]=reg
            i+=1
        print("Done.")
        
    def set_packet_handler(self, handler):
        self.packet_handler = handler
    
    def setup_status(self, registers):
        # Loop over the lines
        # extract the status label
        # extract the lookup register
        # interpet limits if defined
        # units?
        for eachline in registers:
            if('/' in eachline):

    def get_status(self):
        pass

# This is a subunit of a servo allowing the mapping of a name to an address and byte length.
class Register:
    name = None
    address = 0
    data_size = 0
    readonly = False
    packet_handler = None
    port_handler = None
    servo_id = 0
    def __init__(self, name, addr, size, access, protocol, handler, servoId) -> None:
        self.name = name
        self.address = int(addr)
        self.data_size = int(size)
        self.readonly = not ('W' in access)
        self.packet_handler = PacketHandler(protocol)
        self.port_handler = handler
        self.servo_id = servoId
        

    def get_value(self):
        if(self.data_size == 1):
            return self.packet_handler.read1ByteTxRx(self.port_handler,self.servo_id,self.address)
        if(self.data_size == 2):
            return self.packet_handler.read2ByteTxRx(self.port_handler,self.servo_id,self.address)
        if(self.data_size == 4):
            return self.packet_handler.read4ByteTxRx(self.port_handler,self.servo_id,self.address)
        

    def set_value(self, value):
        if(self.readonly):
            print(self.name + ' is readonly.')
            return
        if (self.data_size == 1):
            result, error = self.packet_handler.write1ByteTxRx(self.port_handler, self.servo_id, self.address, value)
            if result != 0:
                print("%s" % self.packet_handler.getTxRxResult(result))
            elif error !=0:
                print("%s" % self.packet_handler.getRxPacketError(error))
        elif (self.data_size == 2):
            result, error = self.packet_handler.write2ByteTxRx(self.port_handler, self.servo_id, self.address, value)
            if result != 0:
                print("%s" % self.packet_handler.getTxRxResult(result))
            elif error !=0:
                print("%s" % self.packet_handler.getRxPacketError(error))
        elif (self.data_size == 4):
            result, error = self.packet_handler.write4ByteTxRx(self.port_handler, self.servo_id, self.address, value)
            if result != 0:
                print("%s" % self.packet_handler.getTxRxResult(result))
            elif error !=0:
                print("%s" % self.packet_handler.getRxPacketError(error))