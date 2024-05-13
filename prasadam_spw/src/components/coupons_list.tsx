import { Card, Heading, List, ListItem } from "@chakra-ui/react"
import { IssueCoupon } from "./window"
import { CouponView } from "./coupon_view"

interface Props {
    coupons: IssueCoupon[],
}


export const CouponsList = ({ coupons }: Props) => {

    if (coupons === undefined || coupons.length === 0) {
        return <p>No Entries</p>
    }
    return <>
        <List spacing={8}>
            {coupons && coupons.map((v) => {
                return <ListItem><CouponView coupon={v} /></ListItem>
            })}
        </List>
    </>
}