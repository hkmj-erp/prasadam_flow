import { Text, Container, Heading, Input, InputGroup, InputLeftAddon, InputRightAddon, Stack, Button, FormControl, FormErrorMessage, FormLabel, Box, Checkbox, Flex, VStack, propNames, Alert, AlertIcon } from "@chakra-ui/react"
import axios from "axios";
import { ErrorMessage, useFormik } from "formik";
import { useFrappePostCall } from "frappe-react-sdk";
import { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

interface FieldProps {
    field: {
        name: string;
        value: any;
        onChange: (event: React.ChangeEvent<any>) => void;
        onBlur: (event: React.FocusEvent<any>) => void;
    };
    form: {
        touched: { [field: string]: boolean };
        errors: { [field: string]: string };
    };
    meta: {
        error?: string;
        touched?: boolean;
    };
}

export const IssueWindow = () => {
    let { id } = useParams();

    const navigate = useNavigate();

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
                "mobile": values.mobile
            })
            actions.setSubmitting(false);
            navigate("/success");
        }
    });
    return (
        <Flex bg="gray.100" align="center" justify="center" h="100vh">
            <Box bg="white" p={6} rounded="md">
                <form onSubmit={formik.handleSubmit}>
                    <VStack spacing={4} align="flex-start">
                        <Text size="xl">Prasadam Coupon Issue Window</Text>
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
                        <Button
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
    );
};