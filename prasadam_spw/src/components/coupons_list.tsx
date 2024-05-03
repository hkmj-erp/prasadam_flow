import { Card, CardBody, Text, Heading, List, ListItem, Stack, Icon } from "@chakra-ui/react"
import { AiOutlineNumber } from "react-icons/ai"
import { FiMapPin } from "react-icons/fi"
import { MdAvTimer } from "react-icons/md"
import { WiTime4 } from "react-icons/wi"
import QRCode from "react-qr-code"

interface IssueCoupon {
    coupon_data: string,
    slot: string,
    venue: string,
    use_date: Date,
    name: string,
    serving_time: string,
    number: number,
    used: number
}

interface Props {
    coupons: IssueCoupon[],
}


export const CouponsList = (props: Props) => {
    return <>
        <Heading my={10}>Coupons</Heading>
        <List spacing={3}>
            {props.coupons.map(coupon => {
                return <ListItem>
                    <Card maxW='sm'>
                        <CardBody>
                            <QRCode
                                size={256}
                                style={{ height: "auto", maxWidth: "100%", width: "100%" }}
                                value={coupon.name}
                                viewBox={`0 0 256 256`}
                            />
                            <Stack mt='6' spacing='3'>
                                <Heading size='md'>{coupon.coupon_data}</Heading>
                                <Text><Icon as={WiTime4} /> {coupon.slot}</Text>
                                <Text><Icon as={FiMapPin} /> {coupon.venue}</Text>
                                <Text><Icon as={MdAvTimer} /> {coupon.serving_time}</Text>
                                <Text><Icon as={AiOutlineNumber} /> {coupon.number - coupon.used} / {coupon.number}</Text>
                            </Stack>
                        </CardBody>
                    </Card>
                </ListItem>
            })}
        </List>
    </>
}