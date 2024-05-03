import { Alert, AlertDescription, AlertIcon, AlertTitle, Box, Center, Container, Heading, Input, Link } from "@chakra-ui/react";

export const Component = () => {
  return <Container>
    <Center>
      <Alert status='success'>
        <AlertIcon />
        <Box>
          <AlertTitle>Success!</AlertTitle>
          <AlertDescription>
            You will receive shortly a WhatsApp Message with details of coupon & QR. Thank you.
          </AlertDescription>
        </Box>
      </Alert>
    </Center>
  </Container>
    ;
};
