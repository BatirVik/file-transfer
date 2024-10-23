"use server";

import config from "@/app/config";
import { NextResponse } from "next/server";

async function uploadFiles(body: FormData) {
  {
  }
  const url = `${config.API_URL}/v1/folders`;
  const response = await fetch(url, {
    method: "POST",
    body,
  });
  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}
