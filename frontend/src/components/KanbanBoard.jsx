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

  user,

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

  const [documents,
    setDocuments] =
    useState({})

  const [documentFiles,
    setDocumentFiles] =
    useState({})

  const token =
    localStorage.getItem(
      "token"
    )

  const canManageTasks =
    user?.role === "admin" ||
    user?.role === "manager"

  const canAddInternalNotes =
    user?.role === "admin" ||
    user?.role === "manager"

  const formatDateTime =
    (value) => {

      if (!value) {

        return "Not set"
      }

      return new Date(value).toLocaleString(
        "en-IN",
        {
          dateStyle: "medium",
          timeStyle: "short"
        }
      )
    }

  const getUserLabel =
    (name, id) => (

      name
        ? `${name} (#${id})`
        : `User #${id}`
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
              response.data.items ||
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


  const fetchDocuments =
    async (taskId) => {

      try {

        const response =
          await axios.get(

            `http://127.0.0.1:8000/documents/task/${taskId}`,

            {
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        setDocuments(
          (prev) => ({

            ...prev,

            [taskId]:
              response.data.items ||
              response.data
          })
        )

      } catch (error) {

        console.error(error)
      }
    }


  const uploadDocument =
    async (taskId) => {

      const file =
        documentFiles[taskId]

      if (!file) {

        const fileInput =
          document.getElementById(
            `document-upload-${taskId}`
          )

        fileInput?.click()

        return
      }

      const formData =
        new FormData()

      formData.append(
        "file",
        file
      )

      try {

        await axios.post(

          `http://127.0.0.1:8000/documents/upload?task_id=${taskId}`,

          formData,

          {
            headers: {
              Authorization:
                `Bearer ${token}`
            }
          }
        )

        setDocumentFiles(
          (prev) => ({

            ...prev,

            [taskId]: null
          })
        )

        const fileInput =
          document.getElementById(
            `document-upload-${taskId}`
          )

        if (fileInput) {

          fileInput.value = ""
        }

        fetchDocuments(taskId)

      } catch (error) {

        console.error(error)

        alert(
          error.response?.data?.detail ||
          "Document upload failed"
        )
      }
    }


  const downloadDocument =
    async (documentItem) => {

      try {

        const response =
          await axios.get(

            `http://127.0.0.1:8000/documents/${documentItem.id}`,

            {
              responseType: "blob",
              headers: {
                Authorization:
                  `Bearer ${token}`
              }
            }
          )

        const url =
          window.URL.createObjectURL(
            new Blob([response.data])
          )

        const link =
          document.createElement("a")

        link.href = url

        link.setAttribute(
          "download",
          documentItem.file_name
        )

        document.body.appendChild(link)

        link.click()

        link.remove()

        window.URL.revokeObjectURL(url)

      } catch (error) {

        console.error(error)

        alert(
          "Document download failed"
        )
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

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">

        {Object.entries(columns)
          .map(

            ([status,
              title]) => {

              const statusTasks =
                tasks.filter(
                  (task) =>

                    task.status
                    === status
                )

              return (

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
                    className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm min-h-[520px]"
                  >

                    <div className="flex items-center justify-between mb-4">

                      <h2 className="text-sm font-bold text-slate-700 tracking-wide">

                        {title}

                      </h2>

                      <span className="bg-slate-100 text-slate-600 border border-slate-200 rounded-full px-2.5 py-1 text-xs font-semibold">

                        {statusTasks.length}

                      </span>

                    </div>

                    <div className="space-y-3 max-h-[68vh] min-h-[440px] overflow-y-auto pr-1 nice-scrollbar">

                      {statusTasks
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

                                  className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm"
                                >

                                  <div className="flex justify-between items-start gap-3">

                                    <div>

                                      <h3 className="font-bold text-base text-slate-900">

                                        {
                                          task.title
                                        }

                                      </h3>

                                      <p className="text-sm text-slate-600 mt-2 leading-5">

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

                                  <div className="mt-4 text-sm text-slate-500 space-y-3">

                                    <div className="grid grid-cols-1 gap-2 bg-slate-50 border border-slate-200 rounded-xl p-3">

                                      <p>

                                        Assigned to:
                                        {" "}
                                        <span className="font-semibold text-slate-700">

                                          {getUserLabel(
                                            task.assigned_to_name,
                                            task.assigned_to
                                          )}

                                        </span>

                                      </p>

                                      <p>

                                        Assigned by:
                                        {" "}
                                        <span className="font-semibold text-slate-700">

                                          {getUserLabel(
                                            task.created_by_name,
                                            task.created_by
                                          )}

                                        </span>

                                      </p>

                                      <p>

                                        Created:
                                        {" "}
                                        <span className="font-semibold text-slate-700">

                                          {formatDateTime(
                                            task.created_at
                                          )}

                                        </span>

                                      </p>

                                      <p>

                                        Due:
                                        {" "}
                                        <span className="font-semibold text-slate-700">

                                          {formatDateTime(
                                            task.due_date
                                          )}

                                        </span>

                                      </p>

                                    </div>

                                    {task.approval_status && (

                                      <div className="bg-slate-50 border border-slate-200 rounded-xl p-3">

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

                                  {canManageTasks && (

                                    <div className="mt-5 flex gap-3">

                                      <button
                                        onClick={() =>
                                          onEdit(
                                            task
                                          )
                                        }
                                        className="flex-1 bg-slate-800 hover:bg-slate-900 text-white py-2 rounded-lg text-sm font-semibold"
                                      >

                                        Edit

                                      </button>

                                      <button
                                        onClick={() =>
                                          onDelete(
                                            task.id
                                          )
                                        }
                                        className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 rounded-lg text-sm font-semibold"
                                      >

                                        Delete

                                      </button>

                                    </div>
                                  )}

                                  <div className="mt-4 border-t border-slate-100 pt-4">

                                    <button
                                      onClick={() =>
                                        fetchDocuments(
                                          task.id
                                        )
                                      }
                                      className="text-sm text-slate-700 hover:text-slate-950 font-semibold"
                                    >

                                      View Documents

                                    </button>

                                    <div className="mt-3 space-y-2 max-h-36 overflow-y-auto pr-1">

                                      {(documents[
                                        task.id
                                      ] || [])
                                        .map(
                                          (
                                            document
                                          ) => (

                                            <div
                                              key={
                                                document.id
                                              }
                                              className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-sm flex items-center justify-between gap-3"
                                            >

                                              <div>

                                                <p className="font-semibold text-gray-700">

                                                  {
                                                    document.file_name
                                                  }

                                                </p>

                                                <p className="text-xs text-gray-500">

                                                  Version
                                                  {" "}
                                                  {
                                                    document.version
                                                  }

                                                </p>

                                              </div>

                                              <button
                                                onClick={() =>
                                                  downloadDocument(
                                                    document
                                                  )
                                                }
                                                className="bg-slate-800 hover:bg-slate-900 text-white px-3 py-2 rounded-lg text-xs font-semibold"
                                              >

                                                Download

                                              </button>

                                            </div>
                                          )
                                        )}
                                    </div>

                                    <div className="mt-3 flex flex-col gap-2">

                                      <input
                                        id={`document-upload-${task.id}`}
                                        type="file"
                                        onChange={(e) =>
                                          setDocumentFiles(
                                            (
                                              prev
                                            ) => ({

                                              ...prev,

                                              [task.id]:
                                                e.target.files?.[0]
                                            })
                                          )
                                        }
                                        className="hidden"
                                      />

                                      {documentFiles[task.id] && (

                                        <p className="text-xs text-gray-500">

                                          Selected:
                                          {" "}
                                          {
                                            documentFiles[task.id].name
                                          }

                                        </p>
                                      )}

                                      <button
                                        onClick={() =>
                                          uploadDocument(
                                            task.id
                                          )
                                        }
                                        className="bg-slate-800 hover:bg-slate-900 text-white px-3 py-2 rounded-lg text-sm font-semibold"
                                      >

                                        {documentFiles[task.id]
                                          ? "Upload Selected Document"
                                          : "Choose Document"}

                                      </button>

                                    </div>

                                  </div>

                                  <div className="mt-4 border-t border-slate-100 pt-4">

                                    <button
                                      onClick={() =>
                                        fetchComments(
                                          task.id
                                        )
                                      }
                                      className="text-sm text-slate-700 hover:text-slate-950 font-semibold"
                                    >

                                      View Comments

                                    </button>

                                    <div className="mt-3 space-y-2 max-h-40 overflow-y-auto pr-1">

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
                                              className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-sm"
                                            >

                                              <div className="flex justify-between items-center">

                                                <div className="flex items-center gap-2">

                                                  <p className="font-semibold text-indigo-700">

                                                    {
                                                      comment.user_name
                                                    }

                                                  </p>

                                                  {comment.is_internal && (

                                                    <span className="bg-amber-100 text-amber-800 text-xs px-2 py-1 rounded-full">

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
                                          className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-300"
                                        />

                                        <button
                                          onClick={() =>
                                            addComment(
                                              task.id
                                            )
                                          }
                                          className="bg-slate-800 hover:bg-slate-900 text-white px-3 py-2 rounded-lg text-sm"
                                        >

                                          Add

                                        </button>

                                      </div>

                                      {canAddInternalNotes && (

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
                                      )}

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
            }
          )}

      </div>

    </DragDropContext>
  )
}

export default KanbanBoard
