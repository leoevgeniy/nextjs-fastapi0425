import Link from 'next/link'
import {Suspense} from "react";

export default async function NotFound() {
    return (
        <div>
            <h2>Not Found</h2>
            <p>Could not find requested resource</p>
            <Suspense fallback={<div>Loading...</div>}>
                <Link href="/">Return Home</Link>
            </Suspense>
        </div>
    )
}