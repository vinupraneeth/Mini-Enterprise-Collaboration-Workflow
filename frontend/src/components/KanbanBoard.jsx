import {

  useState

} from "react"

import axios from "axios"

import {

  DragDropContext,

  Droppable,

  Draggable

} from "@hello-pangea/dnd"

import StatusBadge from "./StatusBadge"

import PriorityBadge from "./PriorityBadge"


function KanbanBoard({

  tasks,

  onStatusChange,

  onEdit,

  onDelete
}) {

  const columns = {

    todo: "TODO",

    in_progress: "IN PROGRESS",

    review: "REVIEW",

    done: "DONE"
  }

  const [comments,
    setComments] =
    useState({})

  const [commentInputs,
    setCommentInputs] =
    useState({})

  const [internalInputs,
    setInternalInputs] =
    useState({})

  const token =
    localStorage.getItem(
      "token"
    )


  const fetchComments =
    async (taskId) => {

      try {

        const response =
          await axios.get(

            `http://127.0.0.1:8000/tasks/${taskId}/comments`,

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setComments(
          (prev) => ({

            ...prev,

            [taskId]:
              response.data
          })
        )

      } catch (error) {

        console.error(error)
      }
    }


  const addComment =
    async (taskId) => {

      const comment =
        commentInputs[taskId]

      if (!comment)
        return

      try {

        await axios.post(

          `http://127.0.0.1:8000/tasks/${taskId}/comments`,

          {
            comment,

            is_internal:
              internalInputs[
                taskId
              ] || false
          },

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        setCommentInputs(
          (prev) => ({

            ...prev,

            [taskId]: ""
          })
        )

        setInternalInputs(
          (prev) => ({

            ...prev,

            [taskId]: false
          })
        )

        fetchComments(taskId)

      } catch (error) {

        console.error(error)
      }
    }


  const handleDragEnd =
    (result) => {

      if (!result.destination)
        return

      const sourceStatus =
        result.source.droppableId

      const destinationStatus =
        result.destination
          .droppableId

      if (
        sourceStatus ===
        destinationStatus
      ) {

        return
      }

      const taskId =
        Number(
          result.draggableId
        )

      onStatusChange(
        taskId,
        destinationStatus
      )
    }


  return (

    <DragDropContext
      onDragEnd={
        handleDragEnd
      }
    >

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        {Object.entries(columns)
          .map(

            ([status,
              title]) => (

              <Droppable
                droppableId={
                  status
                }
                key={status}
              >

                {(provided) => (

                  <div
                    ref={
                      provided.innerRef
                    }
                    {...provided.droppableProps}
                    className="bg-white/70 backdrop-blur-lg rounded-3xl p-5 shadow-xl min-h-[500px]"
                  >

                    <h2 className="text-xl font-bold text-gray-700 mb-5">

                      {title}

                    </h2>

                    <div className="space-y-4">

                      {tasks
                        .filter(
                          (task) =>

                            task.status
                            === status
                        )
                        .map(
                          (
                            task,
                            index
                          ) => (

                            <Draggable
                              key={
                                task.id
                              }
                              draggableId={String(
                                task.id
                              )}
                              index={
                                index
                              }
                            >

                              {(
                                provided
                              ) => (

                                <div
                                  ref={
                                    provided.innerRef
                                  }

                                  {...provided.draggableProps}

                                  {...provided.dragHandleProps}

                                  className="bg-gradient-to-br from-white to-slate-50 border border-slate-200 rounded-2xl p-5 shadow-lg"
                                >

                                  <div className="flex justify-between items-start gap-3">

                                    <div>

                                      <h3 className="font-bold text-lg text-gray-800">

                                        {
                                          task.title
                                        }

                                      </h3>

                                      <p className="text-sm text-gray-600 mt-2">

                                        {
                                          task.description
                                        }

                                      </p>

                                      <div className="mt-3">

                                        <StatusBadge
                                          status={task.status}
                                        />

                                      </div>

                                    </div>

                                    <PriorityBadge
                                      priority={task.priority}
                                    />

                                  </div>

                                  <div className="mt-4 text-sm text-gray-500 space-y-3">

                                    <p>

                                      Due:
                                      {" "}
                                      {
                                        task.due_date
                                      }

                                    </p>

                                    {task.approval_status && (

                                      <div className="bg-slate-100 border border-slate-200 rounded-xl p-3">

                                        <p className="text-xs font-semibold text-gray-500 mb-1">

                                          Latest Review Status

                                        </p>

                                        <p className="text-sm font-semibold text-indigo-700 capitalize">

                                          {task.approval_status}

                                        </p>

                                        {task.approval_remarks && (

                                          <p className="text-sm text-gray-700 mt-2">

                                            {task.approval_remarks}

                                          </p>
                                        )}

                                      </div>
                                    )}

                                  </div>

                                  <div className="mt-5 flex gap-3">

                                    <button
                                      onClick={() =>
                                        onEdit(
                                          task
                                        )
                                      }
                                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl text-sm font-semibold"
                                    >

                                      Edit

                                    </button>

                                    <button
                                      onClick={() =>
                                        onDelete(
                                          task.id
                                        )
                                      }
                                      className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 rounded-xl text-sm font-semibold"
                                    >

                                      Delete

                                    </button>

                                  </div>

                                  <div className="mt-4 border-t pt-4">

                                    <button
                                      onClick={() =>
                                        fetchComments(
                                          task.id
                                        )
                                      }
                                      className="text-sm text-indigo-600 font-semibold"
                                    >

                                      View Comments

                                    </button>

                                    <div className="mt-3 space-y-2 max-h-40 overflow-y-auto">

                                      {(comments[
                                        task.id
                                      ] || [])
                                        .map(
                                          (
                                            comment
                                          ) => (

                                            <div
                                              key={
                                                comment.id
                                              }
                                              className="bg-white border rounded-lg p-3 text-sm"
                                            >

                                              <div className="flex justify-between items-center">

                                                <div className="flex items-center gap-2">

                                                  <p className="font-semibold text-indigo-700">

                                                    {
                                                      comment.user_name
                                                    }

                                                  </p>

                                                  {comment.is_internal && (

                                                    <span className="bg-red-100 text-red-700 text-xs px-2 py-1 rounded-full">

                                                      Internal

                                                    </span>
                                                  )}

                                                </div>

                                                <p className="text-xs text-gray-400">

                                                  {
                                                    new Date(
                                                      comment.created_at
                                                    ).toLocaleString()
                                                  }

                                                </p>

                                              </div>

                                              <p className="text-gray-700 mt-2">

                                                {
                                                  comment.comment
                                                }

                                              </p>

                                            </div>
                                          )
                                        )}
                                    </div>

                                    <div className="mt-3 flex flex-col gap-3">

                                      <div className="flex gap-2">

                                        <input
                                          type="text"
                                          placeholder="Add comment"
                                          value={
                                            commentInputs[
                                              task.id
                                            ] || ""
                                          }
                                          onChange={(e) =>
                                            setCommentInputs(
                                              (
                                                prev
                                              ) => ({

                                                ...prev,

                                                [task.id]:
                                                  e.target
                                                    .value
                                              })
                                            )
                                          }
                                          className="flex-1 border rounded-lg px-3 py-2 text-sm"
                                        />

                                        <button
                                          onClick={() =>
                                            addComment(
                                              task.id
                                            )
                                          }
                                          className="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-2 rounded-lg text-sm"
                                        >

                                          Add

                                        </button>

                                      </div>

                                      <label className="flex items-center gap-2 text-sm text-gray-600">

                                        <input
                                          type="checkbox"
                                          checked={
                                            internalInputs[
                                              task.id
                                            ] || false
                                          }
                                          onChange={(e) =>
                                            setInternalInputs(
                                              (
                                                prev
                                              ) => ({

                                                ...prev,

                                                [task.id]:
                                                  e.target.checked
                                              })
                                            )
                                          }
                                        />

                                        Internal Note

                                      </label>

                                    </div>

                                  </div>

                                </div>
                              )}

                            </Draggable>
                          )
                        )}

                      {
                        provided.placeholder
                      }

                    </div>

                  </div>
                )}

              </Droppable>
            )
          )}

      </div>

    </DragDropContext>
  )
}

export default KanbanBoard