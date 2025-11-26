import { NavLink, Outlet } from "react-router";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from "../components/ui/navigation-menu"


// export default function DefaultLayout() { 
//   return (
//   <main>
//     <NavigationMenu>
//       <NavigationMenuList>

//         <NavigationMenuItem className="px-1 py-2">
//           <NavLink
//               to="/"
//               className={({ isActive }) =>
//                 `px-4 py-2 rounded-md ${isActive ? "bg-violet-950 text-white" : ""}`
//               }> Home
//           </NavLink>
//         </NavigationMenuItem>
//         <span className="text-violet-700">|</span>
//         <NavigationMenuItem className="py-2">
//           <NavLink
//               to="/job-boards"
//               className={({ isActive }) =>
//                 `px-4 py-2 rounded-md ${isActive ? "bg-violet-950 text-white" : ""}`
//               }> Job Boards
//           </NavLink>
//         </NavigationMenuItem>

//       </NavigationMenuList>
//     </NavigationMenu>

//     <div>
//       <Outlet />
//     </div>
//   </main>
// );

// }

export default function DefaultLayout() {
  return (
    <main>
      <nav className="flex items-center justify-between px-6 py-3 border-b border-violet-900">
        {/* Left side: Brand */}
        <div className="text-xl font-bold select-none">
          Jobify
        </div>

        {/* Right side: Navigation */}
        <NavigationMenu>
          <NavigationMenuList className="flex items-center gap-4">

            <NavigationMenuItem>
              <NavLink
                to="/"
                className={({ isActive }) =>
                  `px-4 py-2 ${
                    isActive ? "bg-violet-950 text-white" : ""
                  }`
                }
              >
                Home
              </NavLink>
            </NavigationMenuItem>

            {/* Separator */}
            <span className="text-violet-700">|</span>

            <NavigationMenuItem>
              <NavLink
                to="/job-boards"
                className={({ isActive }) =>
                  `px-4 py-2 ${
                    isActive ? "bg-violet-950 text-white" : ""
                  }`
                }
              >
                Job Boards
              </NavLink>
            </NavigationMenuItem>

          </NavigationMenuList>
        </NavigationMenu>
      </nav>

      <div>
        <Outlet />
      </div>
    </main>
  );
}