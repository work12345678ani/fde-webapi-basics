import {useState, useEffect} from "react";
import {Avatar, AvatarImage} from "~/components/ui/avatar"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import {Button} from "~/components/ui/button"

import {Link} from "react-router";
import { MoveRight } from "lucide-react";

export async function clientLoader() { // keyword determining this is a loader function. We are not calling it manually. It's similar to a keyword
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return {jobBoards}
}


export default function JobBoards({loaderData}: any) {
  return (
    <div>
    <div style={{
      display: "flex",
      justifyContent: "flex-end" 
    }} className="px-2 py-2"> 
      <Button>
        <Link to="/job-boards/new">Add new Job Board</Link>
      </Button>
    </div>
    <Table className="w-1/2">
      <TableHeader>
        <TableRow>
          <TableHead>Logo</TableHead>
          <TableHead>Slug</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
          {loaderData.jobBoards.map(
          (jobBoard: any) => 
            <TableRow key={jobBoard.id}>
              <TableCell>
                {jobBoard.logo_url
                ?  <Avatar><AvatarImage src={jobBoard.logo_url}></AvatarImage></Avatar>
                : <></>}
              </TableCell>
              <TableCell><Link to={`/job-boards/${jobBoard.slug}/job-posts`} className="capitalize">{jobBoard.slug}</Link></TableCell>
            </TableRow>
        )}
      </TableBody>
    </Table>
    </div>
  )
}