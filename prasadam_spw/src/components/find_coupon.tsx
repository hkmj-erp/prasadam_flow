import { Text, Input, InputGroup, InputLeftAddon, Button, FormControl, FormLabel, Box, VStack, Alert, AlertIcon, HStack, PinInput, PinInputField } from "@chakra-ui/react"
import { SingleDatepicker } from "chakra-dayzed-datepicker";
import { useFormik } from "formik";
import { useFrappePostCall } from "frappe-react-sdk";
import moment from "moment";
import { useState } from "react";
import { CouponsList } from "./coupons_list";
import { IssueCoupon } from "./window";

export const FindCoupons = () => {

    const {
        call, error
    } = useFrappePostCall("prasadam_flow.api.v1.window.prasadam_mobile_generate_otp");

    const {
        call: call2, error: error2
    } = useFrappePostCall("prasadam_flow.api.v1.window.prasadam_mobile_get_coupons");

    const [otpBtnVisible, setOtpBtnVisibility] = useState<boolean>(true);
    const [fetchingCoupons, setFetchingCoupons] = useState<boolean>(false);
    const [use_date, setUseDate] = useState(new Date());
    const [coupons, setCoupons] = useState<IssueCoupon[]>([]);

    const sendOtp = async (mobile: string) => {
        await call({
            "mobile": mobile,
        });
        setOtpBtnVisibility(false);
    }

    const getCoupons = async (mobile: string, otp: string) => {
        setFetchingCoupons(true);

        var response = await call2({
            "mobile": mobile,
            "otp": otp,
            "use_date": moment(use_date).local().format("YYYY-MM-DD")
        });
        setCoupons(response.message);
        setFetchingCoupons(false);
    }

    const formik = useFormik({
        initialValues: {
            mobile: "",
        },
        onSubmit: async (values, actions) => {

        }
    });

    return (
        <>
            <Box bg="white" p={6} rounded="md">
                <form onSubmit={formik.handleSubmit}>
                    <VStack spacing={4} align="flex-start">
                        <Text size="xl">Find Prasadam Coupons</Text>
                        <FormControl>
                            <FormLabel htmlFor="use_date">Use Date</FormLabel>
                            <SingleDatepicker
                                name="date-input"
                                date={use_date}

                                onDateChange={setUseDate}

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
                        <Button
                            colorScheme="purple"
                            width="full"
                            isDisabled={!otpBtnVisible}
                            onClick={() => sendOtp(formik.values.mobile)}
                        >
                            Get OTP
                        </Button>
                        <FormControl>
                            <FormLabel htmlFor="otp">OTP</FormLabel>
                            <HStack >
                                <PinInput
                                    isDisabled={otpBtnVisible}
                                    otp
                                    onComplete={async (v) => {
                                        getCoupons(formik.values.mobile, v);
                                    }}>
                                    <PinInputField />
                                    <PinInputField />
                                    <PinInputField />
                                    <PinInputField />
                                    <PinInputField />
                                    <PinInputField />
                                </PinInput>
                            </HStack>
                        </FormControl>

                        {/* <ErrorMessage name="Erro"></ErrorMessage> */}
                        {/* name={error?.exception ?? "Something went wrong!"} */}
                        {error && (
                            <Alert status='error'>
                                <AlertIcon />
                                {error?.exception ?? "Something went wrong!"}
                            </Alert>
                        )}
                        {error2 && (
                            <Alert status='error'>
                                <AlertIcon />
                                {error2?.exception ?? "Something went wrong!"}
                            </Alert>
                        )}
                    </VStack>
                </form>

            </Box>
            <CouponsList coupons={coupons} />
        </>


    );
};