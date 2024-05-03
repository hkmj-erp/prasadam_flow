
import {
	Route,
	RouterProvider,
	createBrowserRouter,
	createRoutesFromElements,
} from "react-router-dom";
import { IssueWindow } from "./components/window";
import { Box } from "@chakra-ui/react";
import { FrappeProvider } from "frappe-react-sdk";
import { FindCoupons } from "./components/find_coupon";

function App() {
	const router = createBrowserRouter(
		createRoutesFromElements(
			<>
				<Route path="/" lazy={() => import("./components/welcome")} />
				<Route path="/success" lazy={() => import("./components/success")} />
				<Route path="/window/:id" element={<IssueWindow />} />
				<Route path="/find_coupons" element={<FindCoupons />} />
			</>
		),
		{
			basename: `/prasadam_spw` ?? "",
		}
	);

	return (
		<>
			<Box p={5}>
				<FrappeProvider>
					<RouterProvider router={router}></RouterProvider>
				</FrappeProvider>

			</Box>
		</>
	);
}

export default App;
