declare module "use-immer" {
  import { Dispatch, SetStateAction } from "react";
  export function useImmer<S>(
    initialValue: S | (() => S),
  ): [S, Dispatch<SetStateAction<S>>];
}
