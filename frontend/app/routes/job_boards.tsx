import {useState, useEffect} from "react";
import {Avatar, AvatarImage} from "~/components/ui/avatar"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "~/components/ui/table";
import {Button} from "~/components/ui/button"

import {Link, useFetcher} from "react-router";
import { MoveRight } from "lucide-react";
import type { Route } from "../+types/root";

export async function clientLoader() { // keyword determining this is a loader function. We are not calling it manually. It's similar to a keyword
  const res = await fetch(`/api/job-boards`);
  const jobBoards = await res.json();
  return {jobBoards}
}

export async function clientAction({ request }: Route.ClientActionArgs) {
  const formData = await request.formData();
  const jobBoardSlug = formData.get("job_board_slug")
  await fetch(`/api/job-boards/${jobBoardSlug}/delete`, {
    method: "DELETE"
  })
}


export default function JobBoards({loaderData}: any) {
  const fetcher = useFetcher();
  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between" 
    }} className="px-2 py-2"> 
      
    <Table className="w-1/2">
      <TableHeader>
        <TableRow>
          <TableHead>Logo</TableHead>
          <TableHead>Slug</TableHead>
          <TableHead>Edit</TableHead>
          <TableHead>Delete</TableHead>
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
              <TableCell>
                <Link to={`/job-boards/${jobBoard.slug}/edit`}>Edit</Link>
              </TableCell>
              <TableCell>
                <fetcher.Form method="post" onSubmit={(event) => {
                      const response = confirm(
                        `Please confirm you want to delete this job board '${jobBoard.slug}'.`,
                      );
                      if (!response) {
                        event.preventDefault();
                      }
                    }}>
                    <input name="job_board_slug" type="hidden" value={jobBoard.slug}></input>
                    <button>Delete</button>
                  </fetcher.Form>
              </TableCell>
            </TableRow>
        )}
      </TableBody>
    </Table>
    <Button>
        <Link to="/job-boards/new">Add new Job Board</Link>
      </Button>
    </div>
  )
}