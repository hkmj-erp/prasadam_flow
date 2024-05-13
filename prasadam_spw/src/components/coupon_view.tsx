import { Card, CardBody, Stack, Heading, Icon, Text, Flex, Box, Spacer, Divider, Tag, HStack, Button, useDisclosure, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, IconButton } from "@chakra-ui/react";
import { AiOutlineNumber } from "react-icons/ai";
import { FiMapPin } from "react-icons/fi";
import { MdAccessTime, MdAvTimer } from "react-icons/md";
import { WiTime4 } from "react-icons/wi";
import QRCode from "react-qr-code";
import { IssueCoupon } from "./window";
import { formatRelative } from "date-fns";
import { ImQrcode } from "react-icons/im";

interface Props {
    coupon: IssueCoupon;
}

export const CouponView = ({ coupon }: Props) => {
    const { isOpen, onOpen, onClose } = useDisclosure()




    return <Card variant="filled">
        <Modal isOpen={isOpen} onClose={onClose}>
            <ModalOverlay />
            <ModalContent>
                <ModalHeader>QR Image</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    <QRCode
                        size={150}
                        style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                        value={coupon.name}
                        viewBox={`0 0 140 140`}
                    />
                </ModalBody>

                <ModalFooter>
                    <Button colorScheme='blue' mr={3} onClick={onClose}>
                        Close
                    </Button>

                </ModalFooter>
            </ModalContent>
        </Modal>
        <CardBody>
            <Heading>{coupon.receiver_name}</Heading>
            <Text fontSize='4xl'>{coupon.receiver_mobile}</Text>
            <Flex mt={4}>
                <Box>
                    <IconButton
                        colorScheme='orange'
                        aria-label='Coupon'
                        size='3xl'
                        p={5}
                        onClick={onOpen}
                        icon={<Icon as={ImQrcode} boxSize={20} />}
                    />
                </Box>
                <Spacer />
                <Box>
                    <Stack spacing='3'>
                        <Heading size='md'>{coupon.coupon_data}</Heading>
                        <Text><Icon as={WiTime4} /> {coupon.slot}</Text>
                        <Text><Icon as={FiMapPin} /> {coupon.venue}</Text>
                        <Text><Icon as={MdAvTimer} /> {coupon.serving_time}</Text>
                        <Text><Icon as={AiOutlineNumber} /> Number : {coupon.number}</Text>
                        <Text><Icon as={AiOutlineNumber} /> Used : {coupon.used}</Text>
                    </Stack>
                </Box>

            </Flex>
            <Heading mt={5} as='h5' size='sm'>
                <HStack><Icon as={MdAccessTime} /> <Text>Issued</Text></HStack>
            </Heading>
            <Tag my={2} bg="yellow.100" ><Text style={{ textTransform: 'capitalize' }} my={2} fontSize="2xl"> {formatRelative(coupon.creation, new Date())}</Text></Tag>

        </CardBody>
    </Card>
}