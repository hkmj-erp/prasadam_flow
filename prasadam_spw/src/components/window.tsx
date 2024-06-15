import { Text, Input, InputGroup, InputLeftAddon, Button, FormControl, FormLabel, Box, Flex, VStack, Alert, AlertIcon, Slider, SliderFilledTrack, SliderThumb, SliderTrack, Tabs, TabPanels, TabList, Tab, TabPanel, StatHelpText, Stat, StatLabel, StatNumber } from "@chakra-ui/react"
import { useFormik } from "formik";
import { useFrappeGetCall, useFrappePostCall } from "frappe-react-sdk";
import React, { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { CouponsList } from "./coupons_list";

export type IssueCoupon = {
    coupon_data: string,
    slot: string,
    venue: string,
    use_date: Date,
    name: string,
    serving_time: string,
    number: number,
    used: number,
    receiver_name: string,
    receiver_mobile: string,
    creation: Date
}

type WindowDetails = {
    limit: number,
    credits?: number,
    recent_issues?: IssueCoupon[]

}

export const IssueWindow = () => {
    let { id } = useParams();

    const { data: windowDetails } = useFrappeGetCall<{ message: WindowDetails }>("prasadam_flow.api.v1.window.get_window_details", { "encrypted_window_id": id });

    const coupons = useMemo(() => {
        if (windowDetails?.message) {
            let v = Object.values(windowDetails.message.recent_issues ?? []);
            return v;
        } else {
            return []
        }
    }, [windowDetails])

    return (
        <Tabs isFitted variant='enclosed'>
            {windowDetails?.message.credits && <TabList mb='1em'>
                <Tab>Issue Coupon</Tab>
                <Tab>Recently Issued Coupons</Tab>
            </TabList>}
            <TabPanels>
                <TabPanel>
                    <NewIssueWindow id={id} windowDetails={windowDetails} />
                </TabPanel>
                {windowDetails?.message.recent_issues && <TabPanel>
                    <CouponsList coupons={coupons} />
                </TabPanel>}
            </TabPanels>
        </Tabs>

    );
};

type NewIssueProps = {
    id?: string,
    windowDetails?: { message: WindowDetails }
}

const NewIssueWindow = ({ id, windowDetails }: NewIssueProps) => {
    const navigate = useNavigate();
    const [couponNumber, setCouponNumber] = React.useState(1)
    const handleChange = (value: React.SetStateAction<number>) => setCouponNumber(value);


    const {
        call, error
    } = useFrappePostCall("prasadam_flow.api.v1.window.get_coupon");

    const formik = useFormik({
        initialValues: {
            full_name: "",
            mobile: ""
        },
        onSubmit: async (values, actions) => {
            await call({
                "encrypted_window_id": id,
                "name": values.full_name,
                "mobile": values.mobile,
                "number": couponNumber
            })
            actions.setSubmitting(false);
            navigate("/success");
        }
    });

    return <>
        <Flex align="center" justify="center" h="70vh">
            <Box bg="white" p={6} rounded="md">
                <form onSubmit={formik.handleSubmit}>
                    <VStack spacing={4} align="flex-start">
                        <Text size="xl">Prasadam Coupon Issue Window</Text>
                        {windowDetails?.message.credits ? <Stat bg='green.100' borderRadius="10" p={2}>
                            <StatLabel>Available Credits</StatLabel>
                            <StatNumber>{windowDetails?.message.credits}</StatNumber>
                            <StatHelpText></StatHelpText>
                        </Stat> : <p></p>}
                        <FormControl>
                            <FormLabel htmlFor="full_name">Full Name</FormLabel>
                            <Input id="full_name"
                                name="full_name"
                                variant="filled"
                                onChange={formik.handleChange}
                                value={formik.values.full_name}
                            />
                        </FormControl>
                        <FormControl>
                            <FormLabel htmlFor="mobile">WhatsApp Number</FormLabel>

                            <InputGroup>
                                <InputLeftAddon>+91</InputLeftAddon>
                                <Input id="mobile"
                                    name="mobile"
                                    type="number"
                                    variant="filled"
                                    onChange={formik.handleChange}
                                    value={formik.values.mobile}
                                    maxLength={10} />
                            </InputGroup>
                        </FormControl>
                        <FormLabel>Number</FormLabel>
                        <Slider
                            focusThumbOnChange={false}
                            value={couponNumber}
                            min={1}
                            max={windowDetails?.message.limit}
                            step={1}
                            onChange={handleChange}
                        >
                            <SliderTrack>
                                <SliderFilledTrack />
                            </SliderTrack>
                            <SliderThumb fontSize='3xl' boxSize={10} children={couponNumber} />
                        </Slider>
                        <Button
                            my={10}
                            type="submit"
                            colorScheme="purple"
                            width="full"
                            isLoading={formik.isSubmitting}
                        >
                            Receive
                        </Button>
                        {/* <ErrorMessage name="Erro"></ErrorMessage> */}
                        {/* name={error?.exception ?? "Something went wrong!"} */}
                        {error && (
                            <Alert status='error'>
                                <AlertIcon />
                                {error?.exception ?? "Something went wrong!"}
                            </Alert>
                        )}
                    </VStack>
                </form>
            </Box>
        </Flex>
    </>
}